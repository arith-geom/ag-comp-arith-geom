module Jekyll
  class MemberPage < Page
    def initialize(site, base, dir, member)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      
      # Initialize data hash with layout
      self.data = {}
      self.data['layout'] = 'member'
      
      # Set page data from member object
      self.data['title'] = member['name']
      self.data['name'] = member['name']
      self.data['role'] = member['role']
      self.data['photo'] = member['photo']
      self.data['email'] = member['email']
      self.data['cv'] = member['cv']
      self.data['files'] = member['files']
      self.data['research_interests'] = member['research_interests']
      self.data['education'] = member['education']
      self.data['links'] = member['links']
      self.data['group'] = member['group']
      self.data['description'] = member['description'] # Short description for card
      self.data['phone'] = member['phone']
      self.data['fax'] = member['fax']
      self.data['room'] = member['room']
      self.data['office_hours'] = member['office_hours']
      self.data['selected_publications'] = member['selected_publications']
      self.data['theses'] = member['theses']
      self.data['theses'] = member['theses']
      self.data['content_match_name'] = member['content_match_name']
      
      # Set default SEO values if missing (matching .pages.yml defaults)
      seo = member['seo'] || {}
      seo['sitemap_priority'] ||= 0.8
      seo['sitemap_changefreq'] ||= 'monthly'
      self.data['seo'] = seo
      
      # Handle body content (rich text)
      self.content = member['body'] || ""
    end
  end

  class MemberGenerator < Generator
    safe true

    def generate(site)
      if site.data['members'] && site.data['members']['sections']
        site.config['generated_members'] = []
        site.data['members']['sections'].each do |section|
          if section['members']
            section['members'].each do |member|
              # Create slug from name using Jekyll's utility to match Liquid filter
              slug = Utils.slugify(member['name'], mode: 'latin')[0..100]

              # Auto-fix relative links in body
              if member['body']
                # Fix markdown links [label](assets/...) -> [label](/assets/...)
                member['body'] = member['body'].gsub(/\]\(assets\//, '](/assets/')
                # Fix HTML links href="assets/..." -> href="/assets/..."
                member['body'] = member['body'].gsub(/href="assets\//, 'href="/assets/')
              end

              # Auto-fix relative links in pdfs and links arrays
              ['pdfs', 'links', 'theses', 'selected_publications', 'files'].each do |key|
                if member[key]
                  member[key].each do |item|
                    if item['file'] && item['file'].start_with?('assets/')
                      item['file'] = '/' + item['file']
                    end
                    if item['url'] && item['url'].start_with?('assets/')
                      item['url'] = '/' + item['url']
                    end
                    if item['link'] && item['link'].start_with?('assets/')
                      item['link'] = '/' + item['link']
                    end
                  end
                end
              end
              
              
              # Create page at /members/:slug/
              page = MemberPage.new(site, site.source, File.join('members', slug), member)
              site.pages << page
              site.config['generated_members'] << page
            end
          end
        end
      end
    end
  end
end
