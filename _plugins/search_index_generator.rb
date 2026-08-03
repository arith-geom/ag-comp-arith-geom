# frozen_string_literal: true

require 'cgi'
require 'json'

module Jekyll
  module SiteSearchIndex
    module_function

    def plain_text(value)
      flattened = case value
                  when Array then value.map { |item| plain_text(item) }.join(' ')
                  when Hash then value.values.map { |item| plain_text(item) }.join(' ')
                  else value.to_s
                  end
      CGI.unescapeHTML(flattened.gsub(%r{<[^>]*>}, ' ').gsub(/\s+/, ' ').strip)
    end

    def add(entries, title:, url:, type:, text: nil)
      return if title.to_s.strip.empty? || url.to_s.strip.empty?

      entries << {
        'title' => plain_text(title),
        'url' => url,
        'type' => type,
        'text' => plain_text(text)
      }
    end

    def semester_slug(year, semester)
      title = if semester == 'Winter'
                format('Winter Semester %<year>s/%<next_year>02d',
                       year: year, next_year: (year.to_i + 1) % 100)
              else
                "Summer Semester #{year}"
              end
      Utils.slugify(title, mode: 'latin')
    end
  end

  class SiteSearchPage < PageWithoutAFile
    def initialize(site, entries)
      super(site, site.source, '', 'search-index.json')
      self.content = JSON.generate(entries)
      self.data = { 'layout' => nil, 'sitemap' => false, 'render_with_liquid' => false }
    end
  end

  class SiteSearchGenerator < Generator
    safe true
    priority :lowest

    def generate(site)
      entries = []
      add_navigation(entries, site)
      add_members(entries, site)
      add_publications(entries, site)
      add_teaching(entries, site)
      add_research(entries, site)
      add_links(entries, site)
      site.pages << SiteSearchPage.new(site, entries)
    end

    private

    def add_navigation(entries, site)
      pages_by_url = site.pages.each_with_object({}) { |page, result| result[page.url] = page }
      Array(site.data['navigation']).each do |item|
        page = pages_by_url[item['url']]
        SiteSearchIndex.add(
          entries,
          title: item['title'],
          url: item['url'],
          type: 'Page',
          text: page&.data&.fetch('description', nil)
        )
      end
    end

    def add_members(entries, site)
      Array(site.data.dig('members', 'sections')).each do |section|
        Array(section['members']).each do |member|
          slug = Utils.slugify(member['name'], mode: 'latin')[0..100]
          SiteSearchIndex.add(
            entries,
            title: member['name'],
            url: "/members/#{slug}/",
            type: 'Member',
            text: member.reject { |key, _value| %w[photo files].include?(key) }
          )
        end
      end
    end

    def add_publications(entries, site)
      Array(site.data.dig('publications', 'publications')).each do |publication|
        slug = Utils.slugify(publication['title'], mode: 'latin')
        SiteSearchIndex.add(
          entries,
          title: publication['title'],
          url: "/publications/#{slug}/",
          type: 'Publication',
          text: publication.reject { |key, _value| %w[pdfs links].include?(key) }
        )
      end
    end

    def add_teaching(entries, site)
      Array(site.data.dig('teaching', 'courses')).each do |year_data|
        year = year_data['year']
        Array(year_data['semesters']).each do |semester_data|
          semester = semester_data['semester']
          semester_slug = SiteSearchIndex.semester_slug(year, semester)
          Array(semester_data['courses']).each do |course|
            course_slug = Utils.slugify(course['title'], mode: 'latin')
            SiteSearchIndex.add(
              entries,
              title: course['title'],
              url: "/teaching/#{year}/#{semester_slug}/#{course_slug}/",
              type: 'Teaching',
              text: [year, semester, course.reject { |key, _value| %w[pdfs links].include?(key) }]
            )
          end
        end
      end
    end

    def add_research(entries, site)
      Array(site.data.dig('research', 'research_areas')).each do |area|
        SiteSearchIndex.add(
          entries,
          title: area['title'],
          url: '/research/',
          type: 'Research',
          text: area['content']
        )
      end
    end

    def add_links(entries, site)
      Array(site.data.dig('links', 'groups')).each do |group|
        SiteSearchIndex.add(
          entries,
          title: group['title'],
          url: '/links/',
          type: 'Links',
          text: group['links']
        )
      end
    end
  end
end
