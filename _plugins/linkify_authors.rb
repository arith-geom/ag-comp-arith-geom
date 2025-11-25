module Jekyll
  module LinkifyAuthorsFilter
    def linkify_authors(input)
      return input if input.nil? || input.empty?

      site = @context.registers[:site]
      members_data = site.data['members']
      
      # Build a mapping of name -> url
      # We want to match:
      # 1. Full Name (e.g. "Prof. Dr. Gebhard Böckle")
      # 2. Publication Name (e.g. "Böckle")
      # 3. Variations?
      
      name_map = {}
      
      # Helper to add to map
      add_to_map = ->(name, url) {
        return if name.nil? || name.empty?
        # Avoid very short names that might be common words (though surnames usually aren't)
        return if name.length < 3 
        name_map[name] = url
      }

      process_member = ->(member) {
        return unless member['name']
        
        # Generate URL
        # Assuming slug is generated from name or we need to find the slug.
        # The members.yml doesn't have the slug directly, but the file structure does?
        # Wait, the members.yml is used to GENERATE the pages.
        # The slug is usually slugified name.
        # Let's look at how the member pages are generated.
        # If I don't have the slug, I might need to slugify the name myself.
        # "Prof. Dr. Gebhard Böckle" -> "prof-dr-gebhard-böckle"
        
        slug = Utils.slugify(member['name'])
        url = "/members/#{slug}/"
        
        add_to_map.call(member['name'], url)
        
        surname = member['publication_name']
        if surname.nil? || surname.empty?
            # Infer surname from name (last word)
            # Remove titles like "Dr.", "Prof." first?
            # Or just take the last part.
            parts = member['name'].split
            surname = parts.last if parts.length > 1
        end
        
        if surname
             add_to_map.call(surname, url)
             add_to_map.call("Dr. #{surname}", url)
             add_to_map.call("Prof. #{surname}", url)
             add_to_map.call("Prof. Dr. #{surname}", url)
             # Also "G. Surname"?
        end
        
        # Add aliases
        if member['aliases']
            member['aliases'].each do |a|
                add_to_map.call(a, url)
            end
        end
      }

      if members_data.is_a?(Hash) && members_data['sections']
        members_data['sections'].each do |section|
          next unless section['members']
          section['members'].each do |member|
            process_member.call(member)
          end
        end
      elsif members_data.is_a?(Array)
         members_data.each do |member|
            process_member.call(member)
         end
      elsif members_data.is_a?(Hash)
         # Fallback if it's a dict of slugs (old format?)
         members_data.each do |slug, member|
             # If member is a hash
             if member.is_a?(Hash)
                 process_member.call(member)
             end
         end
      end

      # Sort keys by length descending to match longest first
      sorted_names = name_map.keys.sort_by { |k| -k.length }

      # Use placeholders to avoid nested links
      # We replace matches with a token, then restore them at the end.
      
      result = input.dup
      replacements = {}
      token_id = 0
      
      sorted_names.each do |name|
        url = name_map[name]
        escaped_name = Regexp.escape(name)
        
        # Match whole words if possible, but be careful with punctuation.
        # \b matches word boundary.
        # We want to match "Name" but not "NameX".
        # And we want to avoid matching inside existing tags (though we assume input is text, 
        # but if we have multiple names, we might have issues if we didn't use placeholders).
        # Since we use placeholders, we just need to match the text.
        
        # We still need to be careful about "Böckle" matching "Böckler".
        # So lookahead/lookbehind for non-word char.
        
        regex = /(?<!\w)#{escaped_name}(?!\w)/
        
        result.gsub!(regex) do |match|
          token = "@@LINK_#{token_id}@@"
          replacements[token] = "<a href=\"#{url}\">#{match}</a>"
          token_id += 1
          token
        end
      end
      
      # Restore replacements
      # We need to do this recursively? No, because we replaced the whole string with a token.
      # But we need to be careful if a token contains another token?
      # No, we replaced the original text with a token. The token doesn't contain the name.
      # So "Prof. Dr. Böckle" -> "@@LINK_0@@".
      # "Böckle" is gone.
      
      replacements.each do |token, replacement|
        result.gsub!(token, replacement)
      end

      result
    end
  end
end

Liquid::Template.register_filter(Jekyll::LinkifyAuthorsFilter)
