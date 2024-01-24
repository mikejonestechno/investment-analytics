c = get_config()
# hide the code input (but include the chart image output)
c.MarkdownExporter.exclude_input=True
# output dir for markdown files relative to working dir NOT notebook dir
c.FilesWriter.build_directory='pages'
# output subdir for image files
c.NbConvertApp.output_files_dir='images'
c.Preprocessor.enabled=True
c.ExecutePreprocessor.enabled=True