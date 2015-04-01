#!/bin/bash

# Check that all tools are available
function checkTool() {
	if [ "`which $1`" == "" ]; then
		echo "Please install $tool first."
		exit 1
	fi
}
checkTool hoedown

# First add the HTML header with CSS styles
cat <<-EOF >doc.html
	<!DOCTYPE html><html>

	<head>
	<meta charset="utf-8">
	<title>CTF@HSO Documentation</title>
	<style type="text/css">
	/**
	 * GitHub2 stylesheet
	 * https://github.com/gcollazo/mou-theme-github2/
	 */
	$(cat style/GitHub2.css)
	</style>
	<style type="text/css">
	$(cat style/prism.css)
	</style>
	</head>
	<body>
EOF

# Build HTML from Markdown
hoedown --all-block --all-flags --all-negative --all-span $1 >>doc.html

# Add Prism for syntax highlighting
cat <<-EOF >>doc.html

	<script type="text/javascript">
	$(cat style/prism.js)
	</script>
	</body>

	</html>
EOF
