locals {
  source_code_dir = "../functions"
}

data "archive_file" "source" {
  type        = "zip"
  source_dir  = local.source_code_dir
  output_path = ".archive/source.zip"
}
