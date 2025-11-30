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
        site.data['publications']['publications'].each do |publication|
          # Create slug from title using Jekyll's utility to match Liquid filter
          slug = Utils.slugify(publication['title'])
          
          # Create page at /publications/:slug/
          site.pages << PublicationPage.new(site, site.source, File.join('publications', slug), publication)
        end
      end
    end
  end
end
