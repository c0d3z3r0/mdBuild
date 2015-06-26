# Documentation Builder

## Build and Install Dependencies

~~~bash
sudo aptitude install wkhtmltopdf

cd /usr/src
git clone https://github.com/hoedown/hoedown
cd hoedown
sudo make install
~~~

## Build the Documentation

Just run `./docbuild.sh` inside the `docbuild` directory.

***Be very careful when copying commands and configs with long lines from the pdf. There will be whitespaces inside. Double check before you execute any command or use the html doc instead.***