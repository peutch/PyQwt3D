MKHOWTO := $(HOME)/CVS/PyQwt/BUILD/Python-2.5.2/Doc/tools/mkhowto

SOURCES := \
	pyqwt3d/configure.help \
	pyqwt3d/copyright.tex \
	pyqwt3d/pyqwt3d.tex


doc: $(SOURCES)
	if [ ! -e html/pyqwt3d ]; then mkdir html/pyqwt3d; fi
	(cd html/pyqwt3d; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -p html/icons/*.png html/pyqwt3d
	python $(MKHOWTO) --html --dir html/pyqwt3d \
	    --image-type png --favicon pyfav.png \
	    --up-link http://pyqwt.sourceforge.net --up-title "PyQwt Home" \
	    pyqwt3d/pyqwt3d.tex
	(cd html/pyqwt3d; rm -f *.dat *.idx *.old *.pl *.gif)
	python nospam.py html/pyqwt3d/*.html
	date -u "+%Y-%m-%d %T" > doc

htdoc: doc $(SOURCES)
	if [ ! -e html/htdoc ]; then mkdir html/htdoc; fi
	(cd html/htdoc; rm -f *.css *.dat *.html *.idx *.old *.pl *.gif)
	cp -pr html/pyqwt3d/* html/htdoc
	python sourceforge.py html/htdoc/*.html
	date -u "+%Y-%m-%d %T" > htdoc

pyqwt3d/configure.help: ../configure/configure.py
	python ../configure/configure.py --help > pyqwt3d/configure.help

# EOF
