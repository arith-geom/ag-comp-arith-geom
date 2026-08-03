# frozen_string_literal: true

module Jekyll
  # Helpers shared by the CMS-backed page generators. All normalization happens
  # on a deep copy so a build never rewrites or mutates the loaded CMS data.
  module GeneratedContentHelpers
    module_function

    def normalized_copy(record, collection_keys:)
      copy = Marshal.load(Marshal.dump(record))
      copy['body'] = normalize_body(copy['body']) if copy['body']

      collection_keys.each do |key|
        next unless copy[key].is_a?(Array)

        copy[key].each do |item|
          next unless item.is_a?(Hash)

          %w[file url link].each do |field|
            item[field] = normalize_asset_path(item[field]) if item[field]
          end
        end
      end

      copy
    end

    def normalize_body(body)
      body.to_s
          .gsub(%r{\]\(assets/}, '](/assets/')
          .gsub(%r{href=(['"])assets/}, 'href=\\1/assets/')
    end

    def normalize_asset_path(path)
      value = path.to_s
      value.start_with?('assets/') ? "/#{value}" : value
    end
  end
end
