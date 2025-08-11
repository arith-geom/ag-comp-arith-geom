# frozen_string_literal: true

# Simple cache-busting filters for assets
# Usage in Liquid: {{ '/assets/css/main.css' | relative_url | bust_css_cache }}

module Jekyll
  module CacheBustFilters
    # Append a version query param based on file mtime
    def bust_file_cache(input)
      append_version_query(input)
    end

    # Alias for CSS assets (same logic)
    def bust_css_cache(input)
      append_version_query(input)
    end

    private

    def append_version_query(input)
      return input if input.to_s.strip.empty?

      begin
        site = @context.registers[:site]
        src = input.to_s
        # Normalize the path on disk (strip any site.baseurl)
        baseurl = site.config['baseurl'].to_s
        src_path = src.start_with?(baseurl) ? src.sub(baseurl, '') : src
        src_path = src_path.sub(%r{^/}, '')
        file_path = File.join(site.source, src_path)

        if File.file?(file_path)
          mtime = File.mtime(file_path).to_i
          separator = src.include?('?') ? '&' : '?'
          return "#{src}#{separator}v=#{mtime}"
        end
      rescue StandardError
        # fall through to return original src
      end

      input
    end
  end
end

Liquid::Template.register_filter(Jekyll::CacheBustFilters)


