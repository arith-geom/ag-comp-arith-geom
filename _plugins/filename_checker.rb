module Jekyll
  class FilenameChecker < Generator
    safe true
    priority :lowest

    def generate(site)
      # Define directories to check
      dirs_to_check = ['assets']

      dirs_to_check.each do |dir|
        path = File.join(site.source, dir)
        next unless File.directory?(path)

        # Recursively find all files
        files = Dir.glob(File.join(path, '**', '*')).select { |f| File.file?(f) }

        files.each do |file|
          relative_path = Pathname.new(file).relative_path_from(Pathname.new(site.source)).to_s
          filename = File.basename(file)

          # Check for non-ASCII characters
          unless filename.ascii_only?
            Jekyll.logger.warn "Filename Warning:", "The file '#{relative_path}' contains special characters. This may cause issues with links. Please rename it to use only letters, numbers, underscores, or hyphens."
          end
        end
      end
    end
  end
end
