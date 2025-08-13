# frozen_string_literal: true

# Pages CMS Integration Plugin for Jekyll
# This plugin provides integration with Pages CMS for content management
# Author: AG Computational Arithmetic Geometry
# Version: 1.0.0

require 'json'
require 'net/http'
require 'uri'
require 'yaml'

module Jekyll
  class PagesCMSIntegration < Jekyll::Generator
    safe true
    priority :high

    def generate(site)
      return unless site.config['pagescms'] && site.config['pagescms']['enabled']

      @site = site
      @config = site.config['pagescms']
      @auto_fix = !!@config['auto_fix']
      
      # Initialize Pages CMS integration
      setup_pagescms_integration
      
      # Process content from Pages CMS
      process_pagescms_content
    end

    private

    def read_front_matter_and_body(file_path)
      content = File.read(file_path)
      # Return empty front matter if no YAML front matter block
      unless content.lstrip.start_with?("---")
        return [{}, content]
      end

      lines = content.lines
      return [{}, content] unless lines[0].strip == '---'

      # Handle accidental duplicate starting delimiter ("---" on both line 1 and 2)
      start_index = 1
      if lines.length > 1 && lines[1].strip == '---'
        # Treat second delimiter as erroneous; begin front matter after it
        start_index = 2
      end

      i = start_index
      front_matter_lines = []
      while i < lines.length && lines[i].strip != '---'
        front_matter_lines << lines[i]
        i += 1
      end

      # Skip the closing delimiter at lines[i]
      i += 1 if i < lines.length && lines[i].strip == '---'

      front_matter_text = front_matter_lines.join
      body = lines[i..-1]&.join || ''

      begin
        fm = YAML.safe_load(front_matter_text) || {}
        fm = {} unless fm.is_a?(Hash)
      rescue
        fm = {}
      end

      [fm, body]
    end

    def write_front_matter_and_body(file_path, front_matter, body)
      # YAML.dump includes the leading '---' line, remove it to avoid duplicates
      begin
        yaml_text = YAML.dump(front_matter.is_a?(Hash) ? front_matter : {})
        yaml_text = yaml_text.sub(/\A---\s*\n/, '')
      rescue
        yaml_text = (front_matter || {}).to_yaml.sub(/\A---\s*\n/, '')
      end

      cleaned_body = body.to_s
      # Avoid accidental extra front matter markers in body
      cleaned_body = cleaned_body.lstrip

      new_content = "---\n#{yaml_text}---\n#{cleaned_body}"
      File.write(file_path, new_content)
    end

    def setup_pagescms_integration
      # Create Pages CMS configuration
      create_pagescms_config
      
      # Setup content synchronization
      setup_content_sync

      if @auto_fix
        Jekyll.logger.info "Pages CMS:", "Auto-fix of front matter is ENABLED (pagescms.auto_fix: true)"
      else
        Jekyll.logger.info "Pages CMS:", "Auto-fix of front matter is DISABLED (pagescms.auto_fix: false)"
      end
    end

    def create_pagescms_config
      # Honor config flag: only generate JSON config if explicitly enabled
      return unless @site.config.dig('pagescms', 'write_generated_config') == true

      # Build dynamic option lists for CMS fields
      # Publication years (descending) as integers to avoid CMS type mismatch
      publication_year_options = (1980..2040).to_a.reverse

      # Teaching semester options up to 2040
      # Use human-friendly labels that our normalizer understands, e.g.:
      #  - "Summer Semester 2025"
      #  - "Winter Semester 2025/26"
      semester_options = []
      (2000..2040).each do |y|
        # Summer semester in same calendar year
        semester_options << "Summer Semester #{y}"
        # Winter semester spans years y/y+1 with two-digit second year
        if y < 2040
          next_two = ((y + 1) % 100).to_s.rjust(2, '0')
          semester_options << "Winter Semester #{y}/#{next_two}"
        end
      end

      config_data = {
        'name' => @site.config['title'] || 'AG Computational Arithmetic Geometry',
        'description' => @site.config['description'] || 'Academic website',
        'version' => '1.0.0',
        'repository' => {
          'repoUrl' => (@site.config.dig('pagescms', 'repo_url') || @site.config['url'] || ''),
          'branch' => (@site.config.dig('pagescms', 'branch') || 'main')
        },
        'contentTypes' => {
          'team-members' => {
            'name' => 'Team Members',
            'description' => 'Faculty, staff, and students',
            'fields' => {
              'name' => {
                'type' => 'string',
                'label' => 'Full Name',
                'required' => true,
                'validation' => {
                  'minLength' => 2,
                  'maxLength' => 100
                }
              },
              'role' => {
                'type' => 'select',
                'label' => 'Role',
                'options' => [
                  'Professor & Group Leader',
                  'Professor',
                  'Postdoctoral Researcher',
                  'PhD Student',
                  'Master Student',
                  'Bachelor Student',
                  'Guest Researcher',
                  'Secretary',
                  'Alumni'
                ],
                'required' => true
              },
              'email' => {
                'type' => 'string',
                'label' => 'Email Address',
                'validation' => {
                  'pattern' => '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
                }
              },
              'photo' => {
                'type' => 'file',
                'label' => 'Profile Photo',
                'accept' => 'image/*',
                'maxSize' => '5MB'
              },
              'research_interests' => {
                'type' => 'text',
                'label' => 'Research Interests',
                'rows' => 3
              },
              'bio' => {
                'type' => 'rich-text',
                'label' => 'Biography'
              },
              'website' => {
                'type' => 'string',
                'label' => 'Website URL',
                'validation' => { 'pattern' => '^https?://.+' }
              },
              'github' => {
                'type' => 'string',
                'label' => 'GitHub Username'
              },
              'orcid' => {
                'type' => 'string',
                'label' => 'ORCID ID'
              },
              'order' => {
                'type' => 'number',
                'label' => 'Sort Order',
                'default' => 100
              },
              'graduation_year' => {
                'type' => 'number',
                'label' => 'Graduation Year'
              },
              'current_position' => {
                'type' => 'string',
                'label' => 'Current Position'
              },
              'status' => {
                'type' => 'select',
                'label' => 'Status',
                'options' => ['active', 'inactive', 'alumni'],
                'default' => 'active'
              }
            }
          },
          'publications' => {
            'name' => 'Publications',
            'description' => 'Research publications and papers',
            'fields' => {
              'title' => {
                'type' => 'string',
                'label' => 'Publication Title',
                'required' => true
              },
              'authors' => {
                'type' => 'string',
                'label' => 'Authors',
                'required' => true
              },
              'year' => {
                'type' => 'select',
                'label' => 'Publication Year',
                'required' => true,
                'options' => publication_year_options
              },
              'type' => {
                'type' => 'select',
                'label' => 'Publication Type',
                'options' => [
                  'Journal Article',
                  'Preprint',
                  'Conference Paper',
                  'Book',
                  'Book Chapter',
                  'Thesis',
                  'Software',
                  'Technical Report'
                ],
                'default' => 'Journal Article'
              },
              'abstract' => {
                'type' => 'text',
                'label' => 'Abstract',
                'rows' => 5
              },
              'doi' => {
                'type' => 'string',
                'label' => 'DOI'
              },
              'url' => {
                'type' => 'string',
                'label' => 'URL',
                'validation' => {
                  'pattern' => '^https?://.+'
                }
              }
            }
          },
          'research' => {
            'name' => 'Research Areas',
            'description' => 'Research areas and projects',
            'fields' => {
              'title' => {
                'type' => 'string',
                'label' => 'Research Area Title',
                'required' => true
              },
              'description' => {
                'type' => 'rich-text',
                'label' => 'Description'
              },
              'keywords' => {
                'type' => 'text',
                'label' => 'Keywords',
                'placeholder' => 'Comma-separated keywords'
              },
              'image' => {
                'type' => 'file',
                'label' => 'Research Area Image',
                'accept' => 'image/*'
              }
            }
          },
          'teaching' => {
            'name' => 'Teaching',
            'description' => 'Courses and teaching materials',
            'fields' => {
              'title' => {
                'type' => 'string',
                'label' => 'Course Title',
                'required' => true
              },
              'semester' => {
                'type' => 'select',
                'label' => 'Semester',
                'required' => true,
                'options' => semester_options
              },
              'course_type' => {
                'type' => 'select',
                'label' => 'Course Type',
                'options' => [
                  'Lecture',
                  'Vorlesung',
                  'Seminar',
                  'Proseminar',
                  'Hauptseminar',
                  'Exercise sessions'
                ]
              },
              'language' => {
                'type' => 'select',
                'label' => 'Language',
                'options' => ['en', 'de'],
                'default' => 'en'
              },
              'instructor' => {
                'type' => 'string',
                'label' => 'Instructor(s)'
              },
              'description' => {
                'type' => 'rich-text',
                'label' => 'Course Description'
              },
              'materials' => {
                'type' => 'file',
                'label' => 'Course Materials',
                'multiple' => true,
                'accept' => '.pdf,.doc,.docx,.ppt,.pptx'
              },
              'active' => {
                'type' => 'select',
                'label' => 'Active',
                'options' => ['true', 'false'],
                'default' => 'false'
              }
            }
          },
          'links' => {
            'name' => 'Links',
            'description' => 'Useful external resources and organizations',
            'fields' => {
              'title' => { 'type' => 'string', 'label' => 'Title', 'required' => true },
              'category' => {
                'type' => 'select',
                'label' => 'Category',
                'options' => [
                  'Tooling',
                  'Research Project',
                  'Research Center',
                  'Institution',
                  'Journal',
                  'Administrative',
                  'Contact'
                ]
              },
              'url' => {
                'type' => 'string',
                'label' => 'URL',
                'validation' => { 'pattern' => '^https?://.+' }
              },
              'description' => { 'type' => 'text', 'label' => 'Description' },
              'order' => { 'type' => 'number', 'label' => 'Sort Order', 'default' => 100 }
            }
          },
          'pages' => {
            'name' => 'Pages',
            'description' => 'Static site pages',
            'fields' => {
              'title' => { 'type' => 'string', 'label' => 'Title', 'required' => true },
              'content' => { 'type' => 'rich-text', 'label' => 'Content' },
              'description' => { 'type' => 'text', 'label' => 'Short Description' }
            }
          }
        }
      }

      # Write Pages CMS configuration
      File.write('pagescms.config.json', JSON.pretty_generate(config_data))
      begin
        File.chmod(0644, 'pagescms.config.json')
      rescue
        # ignore permissions errors on non-POSIX fs
      end
    end

    def setup_content_sync
      # Setup automatic content synchronization if enabled
      if @config['auto_sync']
        Jekyll.logger.info "Pages CMS: Auto-sync enabled"
        
        # Create sync configuration
        sync_config = {
          'enabled' => true,
          'interval' => @config['cache_duration'] || 3600,
          'content_types' => @config['content_types'] || ['members', 'publications', 'research', 'teaching']
        }
        
        # Store sync configuration
        @site.config['pagescms_sync'] = sync_config
      end
    end

    def process_pagescms_content
      # Fetch and sync content from Pages CMS API
      sync_pagescms_content
      
      # Process existing content to ensure compatibility with Pages CMS
      process_members_content
      process_publications_content
      process_research_content
      process_teaching_content
      process_links_content
      process_pages_content

      # Enrich in-memory docs so Liquid sorts immediately on the same build
      enrich_documents_for_sorting
    end

    def sync_pagescms_content
      return unless @config['auto_sync']
      
      Jekyll.logger.info "Pages CMS: Starting content synchronization..."
      
      # Sync each content type
      @config['content_types'].each do |content_type|
        sync_content_type(content_type)
      end
    end

    def sync_content_type(content_type)
      begin
        # Fetch content from Pages CMS API
        content_data = fetch_pagescms_content(content_type)
        
        if content_data && content_data.any?
          Jekyll.logger.info "Pages CMS: Syncing #{content_data.length} #{content_type} items"
          
          # Process each content item
          content_data.each do |item|
            process_pagescms_item(content_type, item)
          end
        else
          Jekyll.logger.info "Pages CMS: No new content for #{content_type}"
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error syncing #{content_type}: #{e.message}"
      end
    end

    def fetch_pagescms_content(content_type)
      # This would normally fetch from Pages CMS API
      # For now, we'll check for new files in the appropriate directories
      case content_type
      when 'members'
        check_new_members
      when 'publications'
        check_new_publications
      when 'research'
        check_new_research
      when 'teaching'
        check_new_teaching
      when 'links'
        check_new_links
      when 'pages'
        check_new_pages
      else
        []
      end
    end

    def check_new_members
      members_dir = File.join(@site.source, '_members')
      return [] unless Dir.exist?(members_dir)
      
      # Check for files modified in the last hour (indicating new content)
      recent_files = Dir.glob(File.join(members_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end
      
      recent_files.map { |file| { 'file' => file, 'type' => 'member' } }
    end

    def check_new_publications
      publications_dir = File.join(@site.source, '_publications')
      return [] unless Dir.exist?(publications_dir)
      
      recent_files = Dir.glob(File.join(publications_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end
      
      recent_files.map { |file| { 'file' => file, 'type' => 'publication' } }
    end

    def check_new_research
      research_dir = File.join(@site.source, '_research')
      return [] unless Dir.exist?(research_dir)
      
      recent_files = Dir.glob(File.join(research_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end
      
      recent_files.map { |file| { 'file' => file, 'type' => 'research' } }
    end

    def check_new_teaching
      teaching_dir = File.join(@site.source, '_teaching')
      return [] unless Dir.exist?(teaching_dir)
      
      recent_files = Dir.glob(File.join(teaching_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end
      
      recent_files.map { |file| { 'file' => file, 'type' => 'teaching' } }
    end

    def check_new_links
      links_dir = File.join(@site.source, '_links')
      return [] unless Dir.exist?(links_dir)

      recent_files = Dir.glob(File.join(links_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end

      recent_files.map { |file| { 'file' => file, 'type' => 'link' } }
    end

    def check_new_pages
      pages_dir = File.join(@site.source, '_pages')
      return [] unless Dir.exist?(pages_dir)

      recent_files = Dir.glob(File.join(pages_dir, '*.md')).select do |file|
        File.mtime(file) > Time.now - 3600
      end

      recent_files.map { |file| { 'file' => file, 'type' => 'page' } }
    end

    def process_pagescms_item(content_type, item)
      begin
        return unless item && item.is_a?(Hash)
        
        file_path = item['file']
        content_type_name = item['type']
        
        return unless file_path && content_type_name
        
        # Read front matter and body safely
        front_matter, body = read_front_matter_and_body(file_path)

        # Ensure proper front matter structure
        front_matter = ensure_front_matter_structure(content_type_name, front_matter)

        # Update the file with proper structure
        update_file_with_front_matter(file_path, front_matter, body)
        
        Jekyll.logger.info "Pages CMS: Processed new #{content_type_name} file: #{File.basename(file_path)}"
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing #{content_type} item: #{e.message}"
      end
    end

    def ensure_front_matter_structure(content_type, front_matter)
      case content_type
      when 'member'
        front_matter['layout'] ||= 'member'
        front_matter['status'] ||= 'active'
        front_matter['role'] ||= 'Member'
      when 'publication'
        front_matter['layout'] ||= 'publication'
        front_matter['type'] ||= 'Journal Article'
        front_matter['status'] ||= 'Published'
      when 'research'
        # There is no dedicated research layout; use the generic page layout
        front_matter['layout'] = 'page'
      when 'teaching'
        front_matter['layout'] ||= 'teaching'
      when 'link'
        # Force generic page layout (avoid missing 'link' layout)
        front_matter['layout'] = 'page'
      when 'page'
        front_matter['layout'] = 'page'
      end
      
      front_matter
    end

    def update_file_with_front_matter(file_path, front_matter, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, front_matter, body)
    end

    def process_members_content
      members_dir = File.join(@site.source, '_members')
      return unless Dir.exist?(members_dir)

      begin
        Dir.glob(File.join(members_dir, '*.md')).each do |file|
          begin
            member_data, body = read_front_matter_and_body(file)

            # Sanitize filenames generated from CMS templates
            begin
              fix_member_filename_if_needed(file, member_data)
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not sanitize member filename #{File.basename(file)}: #{e.message}"
            end
            
            # Ensure member data has required fields for Pages CMS
            member_data['layout'] ||= 'member'
            member_data['status'] ||= 'active'

            # Heuristics to fill missing fields from filename
            begin
              ensure_member_fields(file, member_data)
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not enrich member metadata for #{File.basename(file)}: #{e.message}"
            end
            
            # Update file with standardized front matter
            update_member_file(file, member_data, body)
            
            Jekyll.logger.debug "Pages CMS: Processed member file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing member file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing members directory: #{e.message}"
      end
    end

    def process_publications_content
      publications_dir = File.join(@site.source, '_publications')
      return unless Dir.exist?(publications_dir)

      begin
        Dir.glob(File.join(publications_dir, '*.md')).each do |file|
          begin
            pub_data, body = read_front_matter_and_body(file)

            # Sanitize filenames generated from CMS templates
            begin
              fix_publication_filename_if_needed(file, pub_data)
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not sanitize publication filename #{File.basename(file)}: #{e.message}"
            end
            
            # Ensure publication data has required fields for Pages CMS
            pub_data['layout'] ||= 'publication'
            pub_data['type'] ||= 'Journal Article'

            # Heuristics to fill missing fields from filename
            begin
              ensure_publication_fields(file, pub_data)
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not enrich publication metadata for #{File.basename(file)}: #{e.message}"
            end
            
            # Update file with standardized front matter
            update_publication_file(file, pub_data, body)
            
            Jekyll.logger.debug "Pages CMS: Processed publication file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing publication file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing publications directory: #{e.message}"
      end
    end

    def process_research_content
      research_dir = File.join(@site.source, '_research')
      return unless Dir.exist?(research_dir)

      begin
        Dir.glob(File.join(research_dir, '*.md')).each do |file|
          begin
            research_data, body = read_front_matter_and_body(file)
            
            # Normalize layout to generic page
            if !research_data.key?('layout') || research_data['layout'].to_s.strip.downcase == 'research'
              research_data['layout'] = 'page'
            end
            
            # Fill missing title from filename when needed
            begin
              ensure_title_from_filename(file, research_data, 'title')
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not infer research title for #{File.basename(file)}: #{e.message}"
            end

            # Update file with standardized front matter
            update_research_file(file, research_data, body)
            
            Jekyll.logger.debug "Pages CMS: Processed research file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing research file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing research directory: #{e.message}"
      end
    end

    def process_teaching_content
      teaching_dir = File.join(@site.source, '_teaching')
      return unless Dir.exist?(teaching_dir)

      begin
        Dir.glob(File.join(teaching_dir, '*.md')).each do |file|
          begin
            teaching_data, body = read_front_matter_and_body(file)
            
            # Ensure teaching data has required fields for Pages CMS
            teaching_data['layout'] ||= 'teaching'
            
            # Proactively fix accidental template filenames like
            # "{semester|slugify}-{title|slugify}.md" that may be created by
            # misconfigured CMS templates. We compute a safe target filename
            # from front matter and rename the file if needed.
            begin
              fix_teaching_filename_if_needed(file, teaching_data)
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not sanitize teaching filename #{File.basename(file)}: #{e.message}"
            end

            # Compute normalized semester metadata for reliable sorting/grouping
            begin
              if teaching_data['semester']
                term, sort_year, key = normalize_semester(teaching_data['semester'].to_s)
                if term && sort_year && key
                  teaching_data['semester_term'] = term # 'WS' or 'SS'
                  teaching_data['semester_year'] = sort_year
                  teaching_data['semester_key']  = key   # e.g., 'WS2026'
                  teaching_data['semester_sort'] = (sort_year.to_i * 10) + (term == 'WS' ? 2 : 1)
                end
              end
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not normalize semester for #{File.basename(file)}: #{e.message}"
            end

            # Update file with standardized front matter
            update_teaching_file(file, teaching_data, body)
            
            Jekyll.logger.debug "Pages CMS: Processed teaching file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing teaching file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing teaching directory: #{e.message}"
      end
    end

    def process_links_content
      links_dir = File.join(@site.source, '_links')
      return unless Dir.exist?(links_dir)

      begin
        Dir.glob(File.join(links_dir, '*.md')).each do |file|
          begin
            link_data, body = read_front_matter_and_body(file)

            # Normalize to use generic page layout
            if !link_data.key?('layout') || link_data['layout'].to_s.strip.downcase == 'link'
              link_data['layout'] = 'page'
            end

            # Ensure title/order defaults
            link_data['order'] ||= 100
            begin
              ensure_title_from_filename(file, link_data, 'title')
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not infer link title for #{File.basename(file)}: #{e.message}"
            end

            update_link_file(file, link_data, body)

            Jekyll.logger.debug "Pages CMS: Processed link file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing link file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing links directory: #{e.message}"
      end
    end

    def process_pages_content
      pages_dir = File.join(@site.source, '_pages')
      return unless Dir.exist?(pages_dir)

      begin
        Dir.glob(File.join(pages_dir, '*.md')).each do |file|
          begin
            page_data, body = read_front_matter_and_body(file)

            page_data['layout'] ||= 'page'
            page_data['order'] ||= 100

            # Fill missing title from filename when needed
            begin
              ensure_title_from_filename(file, page_data, 'title')
            rescue => e
              Jekyll.logger.warn "Pages CMS:", "Could not infer page title for #{File.basename(file)}: #{e.message}"
            end

            update_page_file(file, page_data, body)

            Jekyll.logger.debug "Pages CMS: Processed page file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing page file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing pages directory: #{e.message}"
      end
    end

    # Ensure documents have normalized fields required for correct sorting immediately
    def enrich_documents_for_sorting
      begin
        # Teaching normalization in-memory (semester_* fields)
        (@site.collections['teaching']&.docs || []).each do |doc|
          data = doc.data
          next unless data
          s = data['semester']
          next unless s && !s.to_s.strip.empty?
          term, sort_year, key = normalize_semester(s.to_s)
          if term && sort_year && key
            data['semester_term'] ||= term
            data['semester_year'] ||= sort_year
            data['semester_key']  ||= key
            data['semester_sort'] ||= (sort_year.to_i * 10) + (term == 'WS' ? 2 : 1)
          end
        end

        # Members role priority for optional use
        role_priority = {
          'Professor & Group Leader' => 0,
          'Professor' => 1,
          'Postdoctoral Researcher' => 2,
          'PhD Student' => 3,
          'Master Student' => 4,
          'Bachelor Student' => 5,
          'Secretary' => 6,
          'Guest Researcher' => 7,
          'Alumni' => 9
        }
        (@site.collections['members']&.docs || []).each do |doc|
          data = doc.data
          next unless data
          role = data['role'].to_s
          data['role_sort'] ||= role_priority.fetch(role, 99)
          data['order'] ||= 999
        end

        # Deterministic default order for links/pages
        %w[links pages].each do |coll|
          (@site.collections[coll]&.docs || []).each do |doc|
            doc.data['order'] ||= 100
          end
        end
      rescue => e
        Jekyll.logger.warn "Pages CMS:", "Document enrichment failed: #{e.message}"
      end
    end

    def update_member_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    def update_publication_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    def update_research_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    def update_teaching_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    def update_link_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    def update_page_file(file_path, data, body)
      return unless @auto_fix
      write_front_matter_and_body(file_path, data, body)
    end

    # --- Helpers -----------------------------------------------------------

    # If a teaching file name still contains unresolved template tokens
    # (e.g., "{semester|slugify}-{title|slugify}.md"), rename it to a
    # sanitized slug derived from front matter fields.
    def fix_teaching_filename_if_needed(file_path, front_matter)
      basename = File.basename(file_path)
      return unless basename.include?('{') || basename.include?('}') || basename.include?('|')

      semester = front_matter['semester'].to_s.strip
      title    = front_matter['title'].to_s.strip
      return if semester.empty? || title.empty?

      # Use Jekyll's slugify to form a safe filename
      sem_slug = Jekyll::Utils.slugify(semester)
      title_slug = Jekyll::Utils.slugify(title)
      target_basename = "#{sem_slug}-#{title_slug}.md"

      dir = File.dirname(file_path)
      target_path = File.join(dir, target_basename)

      return if File.expand_path(file_path) == File.expand_path(target_path)

      if File.exist?(target_path)
        # If target already exists, disable the original templated file by
        # renaming it so Jekyll won't render it again.
        disabled_path = file_path + ".disabled"
        begin
          File.rename(file_path, disabled_path)
          Jekyll.logger.info "Pages CMS:", "Disabled duplicate templated teaching file #{basename} -> #{File.basename(disabled_path)}"
        rescue => e
          Jekyll.logger.warn "Pages CMS:", "Could not disable duplicate teaching file #{basename}: #{e.message}"
        end
        return
      end

      File.rename(file_path, target_path)
      Jekyll.logger.info "Pages CMS:", "Renamed teaching file #{basename} -> #{target_basename}"
    end

    # Sanitize member filename if templated tokens present
    def fix_member_filename_if_needed(file_path, front_matter)
      basename = File.basename(file_path)
      return unless basename.include?('{') || basename.include?('}') || basename.include?('|')

      name = front_matter['name'].to_s.strip
      # Try to infer from existing filename when name missing
      if name.empty?
        slug = File.basename(file_path, '.md')
        name = slug.split('-').map { |part| part.capitalize }.join(' ')
      end
      return if name.empty?

      target_basename = "#{Jekyll::Utils.slugify(name)}.md"
      dir = File.dirname(file_path)
      target_path = File.join(dir, target_basename)

      return if File.expand_path(file_path) == File.expand_path(target_path)

      if File.exist?(target_path)
        disabled_path = file_path + ".disabled"
        begin
          File.rename(file_path, disabled_path)
          Jekyll.logger.info "Pages CMS:", "Disabled duplicate templated member file #{basename} -> #{File.basename(disabled_path)}"
        rescue => e
          Jekyll.logger.warn "Pages CMS:", "Could not disable duplicate member file #{basename}: #{e.message}"
        end
        return
      end

      File.rename(file_path, target_path)
      Jekyll.logger.info "Pages CMS:", "Renamed member file #{basename} -> #{target_basename}"
    end

    # Sanitize publication filename if templated tokens present
    def fix_publication_filename_if_needed(file_path, front_matter)
      basename = File.basename(file_path)
      return unless basename.include?('{') || basename.include?('}') || basename.include?('|')

      year = front_matter['year']
      title = front_matter['title'].to_s.strip

      # Try infer year/title from filename when missing
      if year.to_s.strip.empty?
        if m = basename.match(/(\d{4})/)
          year = m[1]
        end
      end
      if title.empty?
        title = File.basename(file_path, '.md').sub(/^\d{4}-/, '').gsub('-', ' ').strip
      end

      return if year.to_s.strip.empty? || title.empty?

      target_basename = "#{year}-#{Jekyll::Utils.slugify(title)}.md"
      dir = File.dirname(file_path)
      target_path = File.join(dir, target_basename)

      return if File.expand_path(file_path) == File.expand_path(target_path)

      if File.exist?(target_path)
        disabled_path = file_path + ".disabled"
        begin
          File.rename(file_path, disabled_path)
          Jekyll.logger.info "Pages CMS:", "Disabled duplicate templated publication file #{basename} -> #{File.basename(disabled_path)}"
        rescue => e
          Jekyll.logger.warn "Pages CMS:", "Could not disable duplicate publication file #{basename}: #{e.message}"
        end
        return
      end

      File.rename(file_path, target_path)
      Jekyll.logger.info "Pages CMS:", "Renamed publication file #{basename} -> #{target_basename}"
    end

    # Heuristic enrichment for members
    def ensure_member_fields(file_path, front_matter)
      if front_matter['name'].to_s.strip.empty?
        slug = File.basename(file_path, '.md')
        front_matter['name'] = slug.split('-').map { |part| part.capitalize }.join(' ')
      end
      front_matter['role'] ||= 'Member'
      front_matter['order'] ||= 999
      front_matter
    end

    # Heuristic enrichment for publications
    def ensure_publication_fields(file_path, front_matter)
      if front_matter['title'].to_s.strip.empty?
        base = File.basename(file_path, '.md').sub(/^\d{4}-/, '')
        front_matter['title'] = base.split('-').map { |p| p.capitalize }.join(' ')
      end
      if front_matter['year'].to_s.strip.empty?
        if m = File.basename(file_path).match(/(\d{4})/)
          front_matter['year'] = m[1].to_i
        end
      end
      front_matter
    end

    # Generic title inference
    def ensure_title_from_filename(file_path, front_matter, key)
      if front_matter[key].to_s.strip.empty?
        base = File.basename(file_path, '.md')
        base = base.sub(/^\d{4}-/, '')
        front_matter[key] = base.split('-').map { |p| p.capitalize }.join(' ')
      end
      front_matter
    end

    # Parse various semester formats and return [term, year, key]
    # Supported examples:
    # - 'SS2026', 'WS2026', 'SS26', 'WS26'
    # - 'Summer term 2025', 'Winter term 2023/24', 'Winter Semester 2025'
    def normalize_semester(semester_str)
      s = semester_str.strip
      # Direct SS/WS with 4 or 2 digits
      if m = s.match(/\A(S[US])\s*(\d{2,4})\z/i)
        term = m[1].upcase
        year = m[2].to_i
        year += 2000 if year < 100
        return [term, year, "#{term}#{year}"]
      end

      # Summer/Winter term 2025 or Winter term 2023/24
      if m = s.match(/\A(Summer|Winter)\s+(?:Semester|term)\s+(\d{4})(?:\/(\d{2}))?\z/i)
        season = m[1].downcase
        y1 = m[2].to_i
        y2 = m[3] ? (2000 + m[3].to_i) : nil
        term = season.start_with?('summer') ? 'SS' : 'WS'
        # Winter term spans two years; use second year when given to keep WS later than SS same calendar year
        year = term == 'WS' ? (y2 || y1) : y1
        return [term, year, "#{term}#{year}"]
      end

      # Fallback: detect season keywords and any 4-digit year
      if s =~ /summer/i || s =~ /ss/i
        if y = s[/\d{4}/]
          return ['SS', y.to_i, "SS#{y}"]
        end
      elsif s =~ /winter/i || s =~ /ws/i
        if y = s[/\d{4}/]
          return ['WS', y.to_i, "WS#{y}"]
        end
      end

      # No parse
      [nil, nil, nil]
    end
  end
end 