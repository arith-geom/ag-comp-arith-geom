# frozen_string_literal: true

require 'uri'

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
          
          next unless slug && target

          slug = slug.sub(%r{^/}, '')
          unless slug.match?(/\A[A-Za-z0-9._-]+\z/) && safe_target?(target)
            Jekyll.logger.error 'ShortlinkGenerator:', "Skipped invalid shortlink #{slug.inspect}"
            next
          end

          # Create page at /[slug]/index.html
          site.pages << ShortlinkPage.new(site, site.source, slug, slug, target, title)
        end
      end
    end

    private

    def safe_target?(target)
      value = target.to_s.strip
      return true if value.start_with?('/') && !value.start_with?('//')

      uri = URI.parse(value)
      %w[http https].include?(uri.scheme) && !uri.host.to_s.empty?
    rescue URI::InvalidURIError
      false
    end
  end
end
