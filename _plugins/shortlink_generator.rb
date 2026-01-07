module Jekyll
  class ShortlinkPage < Page
    def initialize(site, base, dir, slug, target, title)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      self.data = {}
      
      # Minimal layout just for the redirect
      self.data['layout'] = 'redirect'
      
      # Pass data to layout
      self.data['target'] = target
      self.data['title']  = title || "Redirecting..."
      self.data['sitemap'] = false # Do not include redirects in sitemap
    end
  end

  class ShortlinkGenerator < Generator
    safe true

    def generate(site)
      if site.data['shortlinks'] && site.data['shortlinks']['shortlinks']
        site.data['shortlinks']['shortlinks'].each do |link|
          slug = link['slug']
          target = link['target']
          title = link['title']
          
          if slug && target
            # Ensure slug doesn't start with /
            slug = slug.sub(/^\//, '')
            
            # Create page at /[slug]/index.html
            site.pages << ShortlinkPage.new(site, site.source, slug, slug, target, title)
          end
        end
      end
    end
  end
end
