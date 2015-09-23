# mdBuild MarkDown Document builder

mdBuild comes from the CTF@HSO project and was originally the documentation build tool.
Now I use it as a simple MarkDown document builder.

## Build and Install Dependencies

~~~bash
sudo aptitude install wkhtmltopdf

cd /usr/src
git clone https://github.com/hoedown/hoedown
cd hoedown
sudo make install
~~~

## Usage

~~~bash
./mdbuild.py <output_filename> <document1.md> <document2.md ...>
~~~

## Caveats

Be very careful when copying commands and configs with long lines from the pdf.
There will be whitespaces inside. Double check before you execute any command
or use the html doc instead.

## License

Copyright (C) 2015 Michael Niewöhner

This is open source software, licensed under the MIT License. See the file LICENSE for details.