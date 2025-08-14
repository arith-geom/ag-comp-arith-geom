# Jekyll Search Data Generator
# Generates comprehensive search data from all content types

require 'cgi'

module Jekyll
  class SearchGenerator < Generator
    safe true
    priority :high

    def generate(site)
      search_data = []
      
      # Use Jekyll's own slugify for consistency with Liquid
      slugify = lambda { |str| Jekyll::Utils.slugify(str.to_s) }

      # Add pages
      site.pages.each do |page|
        next if page.data['layout'] == 'none' || page.data['layout'] == 'redirect'
        
        content = extract_content(page)
        next if content.strip.empty?
        
        search_data << {
          'id' => "page-#{page.url}",
          'title' => page.data['title'] || page.name,
          'content' => content,
          'url' => page.url,
          'category' => 'page',
          'description' => page.data['description'] || '',
          'tags' => Array(page.data['tags']).join(', '),
          'date' => page.data['date'],
          'layout' => page.data['layout']
        }
      end
      
      # Add posts/news
      site.posts.docs.each do |post|
        content = extract_content(post)
        next if content.strip.empty?
        
        search_data << {
          'id' => "post-#{post.id}",
          'title' => post.data['title'] || post.name,
          'content' => content,
          'url' => post.url,
          'category' => 'news',
          'description' => post.data['description'] || '',
          'tags' => Array(post.data['tags']).join(', '),
          'date' => post.data['date'],
          'author' => post.data['author'] || ''
        }
      end
      
      # Add members
      site.collections['members']&.docs&.each do |member|
        content = extract_content(member)
        next if content.strip.empty?
        status = (member.data['status'] || '').to_s.downcase
        # Navigation rule: alumni/former -> Members page, active -> individual page
        target_url = if status == 'alumni' || status == 'former'
          '/members/?section=alumni'
        else
          member.url
        end
        
        search_data << {
          'id' => "member-#{member.data['name'] || member.basename}",
          'title' => member.data['name'] || member.data['title'] || member.name,
          'content' => content,
          'url' => target_url,
          'category' => 'member',
          'description' => member.data['description'] || member.data['bio'] || '',
          'tags' => Array(member.data['tags']).join(', '),
          'position' => member.data['position'] || '',
          'email' => member.data['email'] || '',
          'research_interests' => member.data['research_interests'] || '',
          'status' => status,
          'role' => member.data['role'] || ''
        }
      end
      
      # Add teaching
      site.collections['teaching']&.docs&.each do |teaching|
        content = extract_content(teaching)
        next if content.strip.empty?
        q = CGI.escape(teaching.data['title'].to_s)
        # Always route to teaching page with a filter query
        target_url = "/teaching/?q=#{q}"
        
        search_data << {
          'id' => "teaching-#{teaching.data['title'] || teaching.basename}",
          'title' => teaching.data['title'] || teaching.name,
          'content' => content,
          'url' => target_url,
          'category' => 'teaching',
          'description' => teaching.data['description'] || '',
          'tags' => Array(teaching.data['tags']).join(', '),
          'semester' => teaching.data['semester'] || '',
          'instructor' => teaching.data['instructor'] || '',
          'course_type' => teaching.data['course_type'] || '',
          'semester_year' => teaching.data['semester_year'] || '',
          'semester_key' => teaching.data['semester_key'] || ''
        }
      end
      
      # Add research
      site.collections['research']&.docs&.each do |research|
        content = extract_content(research)
        next if content.strip.empty?
        
        search_data << {
          'id' => "research-#{research.data['title'] || research.basename}",
          'title' => research.data['title'] || research.name,
          'content' => content,
          'url' => research.url,
          'category' => 'research',
          'description' => research.data['description'] || '',
          'tags' => Array(research.data['tags']).join(', '),
          'area' => research.data['area'] || '',
          'collaborators' => research.data['collaborators'] || ''
        }
      end
      
      # Add publications: open via Publications page filter/detail
      site.collections['publications']&.docs&.each do |pub|
        content = extract_content(pub)
        next if content.strip.empty?

        title = pub.data['title'] || pub.name
        year = pub.data['year'] || ''
        key = [slugify.call(title), year].reject { |v| v.to_s.empty? }.join('-')
        pub_url = "/publications/?pub=#{CGI.escape(key)}"

        search_data << {
          'id' => "publication-#{key}",
          'title' => title,
          'content' => content,
          'url' => pub_url,
          'category' => 'publication',
          'description' => pub.data['abstract'] || pub.data['description'] || '',
          'tags' => Array(pub.data['keywords']).join(', '),
          'authors' => pub.data['authors'] || '',
          'year' => year,
          'journal' => pub.data['journal'] || '',
          'type' => pub.data['type'] || '',
          'status' => pub.data['status'] || ''
        }
      end
      
      # Add links
      site.collections['links']&.docs&.each do |link|
        content = extract_content(link)
        next if content.strip.empty?
        
        search_data << {
          'id' => "link-#{link.data['title'] || link.basename}",
          'title' => link.data['title'] || link.name,
          'content' => content,
          'url' => link.data['url'] || link.url,
          'category' => 'link',
          'description' => link.data['description'] || '',
          'tags' => Array(link.data['tags']).join(', ')
        }
      end
      
      # Write JSON to source and destination to ensure it is served and survives clean
      # 1) Source: allows Jekyll to treat it as a static file and copy to dest
      source_assets_path = File.join(site.source, 'assets')
      FileUtils.mkdir_p(source_assets_path)
      File.write(File.join(source_assets_path, 'search-data.json'), search_data.to_json)

      # 2) Destination: make it immediately available during the same build
      site_assets_path = File.join(site.dest, 'assets')
      FileUtils.mkdir_p(site_assets_path)
      File.write(File.join(site_assets_path, 'search-data.json'), search_data.to_json)
      
      puts "Generated search data for #{search_data.length} items"
    end
    
    private
    
    def extract_content(page)
      # Extract text content from page/post
      content = page.content || ''
      
      # Remove HTML tags and markdown syntax
      content = content.gsub(/<[^>]*>/, ' ') # Remove HTML tags
      content = content.gsub(/\[([^\]]*)\]\([^)]*\)/, '\1') # Convert markdown links to text
      content = content.gsub(/!\[([^\]]*)\]\([^)]*\)/, '\1') # Convert markdown images to alt text
      content = content.gsub(/[*_`~#]+/, ' ') # Remove markdown formatting
      content = content.gsub(/\n+/, ' ') # Replace newlines with spaces
      content = content.gsub(/\s+/, ' ') # Normalize whitespace
      
      # Add front matter data to content for better search
      front_matter_content = []
      page.data.each do |key, value|
        next if ['layout', 'permalink', 'published'].include?(key)
        if value.is_a?(String) && !value.empty?
          front_matter_content << value
        elsif value.is_a?(Array)
          front_matter_content << value.join(' ')
        end
      end
      
      full_content = [content, front_matter_content.join(' ')].join(' ')
      full_content.strip
    end
  end
end 