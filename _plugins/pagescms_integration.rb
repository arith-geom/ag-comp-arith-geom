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
      
      # Initialize Pages CMS integration
      setup_pagescms_integration
      
      # Process content from Pages CMS
      process_pagescms_content
    end

    private

    def setup_pagescms_integration
      # Create Pages CMS configuration
      create_pagescms_config
      
      # Setup content synchronization
      setup_content_sync
    end

    def create_pagescms_config
      config_data = {
        'name' => @site.config['title'] || 'AG Computational Arithmetic Geometry',
        'description' => @site.config['description'] || 'Academic website',
        'version' => '1.0.0',
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
                  'Professor',
                  'Postdoctoral Researcher',
                  'PhD Student',
                  'Master Student',
                  'Bachelor Student',
                  'Guest Researcher',
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
              'research' => {
                'type' => 'text',
                'label' => 'Research Interests',
                'rows' => 3
              },
              'bio' => {
                'type' => 'rich-text',
                'label' => 'Biography'
              },
              'status' => {
                'type' => 'select',
                'label' => 'Status',
                'options' => ['Active', 'Inactive', 'Alumni'],
                'default' => 'Active'
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
                'type' => 'number',
                'label' => 'Publication Year',
                'required' => true
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
                'type' => 'string',
                'label' => 'Semester',
                'required' => true
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
              }
            }
          }
        }
      }

      # Write Pages CMS configuration
      File.write('pagescms.config.json', JSON.pretty_generate(config_data))
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

    def process_pagescms_item(content_type, item)
      begin
        return unless item && item.is_a?(Hash)
        
        file_path = item['file']
        content_type_name = item['type']
        
        return unless file_path && content_type_name
        
        # Read the file content
        content = File.read(file_path)
        front_matter = YAML.load_file(file_path)
        
        # Skip if YAML loading failed or returned nil
        return unless front_matter && front_matter.is_a?(Hash)
        
        # Ensure proper front matter structure
        front_matter = ensure_front_matter_structure(content_type_name, front_matter)
        
        # Update the file with proper structure
        update_file_with_front_matter(file_path, front_matter, content)
        
        Jekyll.logger.info "Pages CMS: Processed new #{content_type_name} file: #{File.basename(file_path)}"
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing #{content_type} item: #{e.message}"
      end
    end

    def ensure_front_matter_structure(content_type, front_matter)
      case content_type
      when 'member'
        front_matter['layout'] ||= 'member'
        front_matter['status'] ||= 'Active'
        front_matter['role'] ||= 'Member'
      when 'publication'
        front_matter['layout'] ||= 'publication'
        front_matter['type'] ||= 'Journal Article'
        front_matter['status'] ||= 'Published'
      when 'research'
        front_matter['layout'] ||= 'research'
        front_matter['status'] ||= 'Active'
      when 'teaching'
        front_matter['layout'] ||= 'teaching'
        front_matter['status'] ||= 'Active'
        front_matter['active'] ||= false
      end
      
      front_matter
    end

    def update_file_with_front_matter(file_path, front_matter, original_content)
      # Extract body content (everything after front matter)
      body_content = original_content.split('---', 3).last || ''
      
      # Create new content with proper front matter
      new_content = "---\n#{front_matter.to_yaml}---\n#{body_content}"
      
      # Write back to file
      File.write(file_path, new_content)
    end

    def process_members_content
      members_dir = File.join(@site.source, '_members')
      return unless Dir.exist?(members_dir)

      begin
        Dir.glob(File.join(members_dir, '*.md')).each do |file|
          begin
            member_data = YAML.load_file(file)
            
            # Skip if YAML loading failed or returned nil
            next unless member_data && member_data.is_a?(Hash)
            
            # Ensure member data has required fields for Pages CMS
            member_data['layout'] ||= 'member'
            member_data['status'] ||= 'Active'
            
            # Update file with standardized front matter
            update_member_file(file, member_data)
            
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
            pub_data = YAML.load_file(file)
            
            # Skip if YAML loading failed or returned nil
            next unless pub_data && pub_data.is_a?(Hash)
            
            # Ensure publication data has required fields for Pages CMS
            pub_data['layout'] ||= 'publication'
            pub_data['type'] ||= 'Journal Article'
            
            # Update file with standardized front matter
            update_publication_file(file, pub_data)
            
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
            research_data = YAML.load_file(file)
            
            # Skip if YAML loading failed or returned nil
            next unless research_data && research_data.is_a?(Hash)
            
            # Ensure research data has required fields for Pages CMS
            research_data['layout'] ||= 'research'
            
            # Update file with standardized front matter
            update_research_file(file, research_data)
            
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
            teaching_data = YAML.load_file(file)
            
            # Skip if YAML loading failed or returned nil
            next unless teaching_data && teaching_data.is_a?(Hash)
            
            # Ensure teaching data has required fields for Pages CMS
            teaching_data['layout'] ||= 'teaching'
            
            # Update file with standardized front matter
            update_teaching_file(file, teaching_data)
            
            Jekyll.logger.debug "Pages CMS: Processed teaching file #{file}"
          rescue => e
            Jekyll.logger.warn "Pages CMS: Error processing teaching file #{file}: #{e.message}"
          end
        end
      rescue => e
        Jekyll.logger.error "Pages CMS: Error processing teaching directory: #{e.message}"
      end
    end

    def update_member_file(file_path, data)
      content = File.read(file_path)
      front_matter = data.to_yaml
      body = content.split('---', 3).last || ''
      
      new_content = "---\n#{front_matter}---\n#{body}"
      File.write(file_path, new_content)
    end

    def update_publication_file(file_path, data)
      content = File.read(file_path)
      front_matter = data.to_yaml
      body = content.split('---', 3).last || ''
      
      new_content = "---\n#{front_matter}---\n#{body}"
      File.write(file_path, new_content)
    end

    def update_research_file(file_path, data)
      content = File.read(file_path)
      front_matter = data.to_yaml
      body = content.split('---', 3).last || ''
      
      new_content = "---\n#{front_matter}---\n#{body}"
      File.write(file_path, new_content)
    end

    def update_teaching_file(file_path, data)
      content = File.read(file_path)
      front_matter = data.to_yaml
      body = content.split('---', 3).last || ''
      
      new_content = "---\n#{front_matter}---\n#{body}"
      File.write(file_path, new_content)
    end
  end
end 