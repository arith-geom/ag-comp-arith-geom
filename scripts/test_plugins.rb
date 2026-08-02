#!/usr/bin/env ruby
# frozen_string_literal: true

require "minitest/autorun"
require "jekyll"
require_relative "../_plugins/generated_content_helpers"
require_relative "../_plugins/linkify_authors"
require_relative "../_plugins/shortlink_generator"

class GeneratedContentHelpersTest < Minitest::Test
  def test_normalization_does_not_mutate_cms_data
    source = {
      "body" => '[File](assets/example.pdf) <a href="assets/other.pdf">Other</a>',
      "links" => [{ "url" => "assets/example.pdf" }]
    }

    normalized = Jekyll::GeneratedContentHelpers.normalized_copy(
      source,
      collection_keys: ["links"]
    )

    assert_equal "assets/example.pdf", source.dig("links", 0, "url")
    assert_includes source["body"], "href=\"assets/"
    assert_equal "/assets/example.pdf", normalized.dig("links", 0, "url")
    assert_includes normalized["body"], "href=\"/assets/"
  end
end

class SanitizeUrlFilterTest < Minitest::Test
  include Jekyll::SanitizeUrlFilter

  def test_blocks_active_content_schemes_and_obfuscated_whitespace
    assert_equal "#", sanitize_url("java\nscript:alert(1)")
    assert_equal "#", sanitize_url("DATA:text/html,example")
    assert_equal "#", sanitize_url("vbscript:example")
  end

  def test_preserves_normal_links
    assert_equal "https://example.org", sanitize_url("https://example.org")
    assert_equal "/publications/", sanitize_url("/publications/")
  end
end

class ShortlinkGeneratorTest < Minitest::Test
  def setup
    @generator = Jekyll::ShortlinkGenerator.new
  end

  def test_accepts_internal_and_https_targets
    assert @generator.send(:safe_target?, "/teaching/")
    assert @generator.send(:safe_target?, "https://example.org/path")
  end

  def test_rejects_protocol_relative_and_active_content_targets
    refute @generator.send(:safe_target?, "//example.org/path")
    refute @generator.send(:safe_target?, "javascript:alert(1)")
  end
end
