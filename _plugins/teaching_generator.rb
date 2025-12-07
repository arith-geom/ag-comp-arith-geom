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
      
      # Handle body content (rich text)
      self.content = course['body'] || ""
    end
  end

  class TeachingGenerator < Generator
    safe true

    def generate(site)
      if site.data['teaching'] && site.data['teaching']['courses']
        site.data['teaching']['courses'].each do |year_data|
          year = year_data['year']
          if year_data['semesters']
            year_data['semesters'].each do |semester_data|
              semester = semester_data['semester']
              if semester_data['courses']
                semester_data['courses'].each do |course|
                  # Create slug from title
                  slug = Utils.slugify(course['title'])

                  # Auto-fix relative links in body
                  if course['body']
                    # Fix markdown links [label](assets/...) -> [label](/assets/...)
                    course['body'] = course['body'].gsub(/\]\(assets\//, '](/assets/')
                    # Fix HTML links href="assets/..." -> href="/assets/..."
                    course['body'] = course['body'].gsub(/href="assets\//, 'href="/assets/')
                  end

                  # Auto-fix relative links in pdfs and links arrays
                  ['pdfs', 'links'].each do |key|
                    if course[key]
                      course[key].each do |item|
                        if item['file'] && item['file'].start_with?('assets/')
                          item['file'] = '/' + item['file']
                        end
                        if item['url'] && item['url'].start_with?('assets/')
                          item['url'] = '/' + item['url']
                        end
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
                  
                  semester_slug = Utils.slugify(semester_title)
                  
                  # Create page at /teaching/:year/:semester/:slug/ to ensure uniqueness
                  site.pages << TeachingPage.new(site, site.source, File.join('teaching', year.to_s, semester_slug, slug), course, year, semester)
                end
              end
            end
          end
        end
      end
    end
  end
end
