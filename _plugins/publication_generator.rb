# frozen_string_literal: true

require_relative 'generated_content_helpers'

module Jekyll
  class PublicationPage < Page
    def initialize(site, base, dir, publication)
      @site = site
      @base = base
      @dir  = dir
      @name = 'index.html'

      self.process(@name)
      
      # Initialize data hash with layout
      self.data = {}
      self.data['layout'] = 'publication_subpage'
      
      # Set page data from publication object
      self.data['title'] = publication['title']
      self.data['authors'] = publication['authors']
      self.data['journal_details'] = publication['journal_details']
      self.data['status'] = publication['status']
      self.data['type'] = publication['type']
      self.data['mr_number'] = publication['mr_number']
      self.data['year'] = publication['year']
      description_parts = [publication['authors'], publication['journal_details']]
                          .compact
                          .map { |part| part.to_s.gsub(%r{<[^>]*>}, ' ').gsub(/\s+/, ' ').strip }
                          .reject(&:empty?)
      self.data['description'] = description_parts.join('. ')

      self.data['reviewer'] = publication['reviewer']
      self.data['citation_count'] = publication['citation_count']
      self.data['publisher_details'] = publication['publisher_details']
      self.data['isbn'] = publication['isbn']
      self.data['appendix'] = publication['appendix']
      self.data['links'] = publication['links']
      self.data['pdfs'] = publication['pdfs']

      
      # Handle body content (rich text)
      self.content = publication['body'] || ""
    end
  end

  class PublicationGenerator < Generator
    safe true

    def generate(site)
      if site.data['publications'] && site.data['publications']['publications']
        site.config['generated_publications'] = []
        site.data['publications']['publications'].each do |source_publication|
          publication = GeneratedContentHelpers.normalized_copy(
            source_publication,
            collection_keys: %w[pdfs links]
          )

          # Create slug from title using Jekyll's utility to match Liquid filter
          slug = Utils.slugify(publication['title'], mode: 'latin')

          # Create page at /publications/:slug/
          page = PublicationPage.new(site, site.source, File.join('publications', slug), publication)
          site.pages << page
          site.config['generated_publications'] << page
        end
      end
    end
  end
end
