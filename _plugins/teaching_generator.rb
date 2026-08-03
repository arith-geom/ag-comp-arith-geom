# frozen_string_literal: true

require 'cgi'
require_relative 'generated_content_helpers'

module Jekyll
  class TeachingPage < Page
    def initialize(site, base, dir, course, year, semester)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      
      # Initialize data hash with layout
      self.data = {}
      self.data['layout'] = 'teaching_subpage'
      
      # Set page data from course object
      self.data['title'] = course['title']
      self.data['instructor'] = course['instructor']
      self.data['course_type'] = course['course_type']
      self.data['description'] = course['description']
      self.data['links'] = course['links']
      self.data['pdfs'] = course['pdfs']
      self.data['year'] = year
      self.data['semester'] = semester
      
      # Set default SEO values if missing (matching .pages.yml defaults)
      seo = course['seo'] || {}
      seo['sitemap_priority'] ||= 0.6
      seo['sitemap_changefreq'] ||= 'monthly'
      self.data['seo'] = seo

      
      # Handle body content (rich text)
      self.content = course['body'] || ""
    end
  end

  class TeachingGenerator < Generator
    safe true

    def generate(site)
      if site.data['teaching'] && site.data['teaching']['courses']
        site.config['generated_teaching'] = []
        site.data['teaching']['courses'].each do |year_data|
          year = year_data['year']
          if year_data['semesters']
            year_data['semesters'].each do |semester_data|
              semester = semester_data['semester']
              if semester_data['courses']
                semester_data['courses'].each do |source_course|
                  course = GeneratedContentHelpers.normalized_copy(
                    source_course,
                    collection_keys: %w[pdfs links]
                  )

                  # Create slug from title
                  slug = Utils.slugify(course['title'], mode: 'latin')

                  if course['body']
                    # Proactively fix member links with non-ASCII characters or encoding
                    # This ensures that even if hardcoded in CMS, they match the new 'latin' slug format
                    course['body'] = course['body'].gsub(/\/members\/([^\/)]+)\//) do |match|
                      begin
                        member_slug = $1
                        # Unescape any percent-encoded characters (like %C3%B6)
                        decoded_slug = CGI.unescape(member_slug)
                        # Re-slugify using 'latin' mode
                        new_slug = Utils.slugify(decoded_slug, mode: 'latin')
                        "/members/#{new_slug}/"
                      rescue StandardError => e
                        Jekyll.logger.warn "TeachingGenerator:", "Failed to process member link #{match}: #{e.message}"
                        match
                      end
                    end
                  end

                  # Generate full semester title for slug to match Liquid template
                  semester_title = semester
                  if semester == "Winter"
                    next_year = year.to_i + 1
                    next_year_short = next_year % 100
                    if next_year_short < 10
                      next_year_short = "0#{next_year_short}"
                    end
                    semester_title = "Winter Semester #{year}/#{next_year_short}"
                  elsif semester == "Summer"
                    semester_title = "Summer Semester #{year}"
                  end
                  
                  semester_slug = Utils.slugify(semester_title, mode: 'latin')
                  
                  # Create page at /teaching/:year/:semester/:slug/ to ensure uniqueness
                  page = TeachingPage.new(site, site.source, File.join('teaching', year.to_s, semester_slug, slug), course, year, semester)
                  site.pages << page
                  site.config['generated_teaching'] << page
                end
              end
            end
          end
        end
      end
    end
  end
end
