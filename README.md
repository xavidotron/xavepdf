# xavepdf
Scripts I made for hacking things out of PDFs.

* `rmimg.py`: interactively remove images and other objects from a PDF.  The
  regexps probably work best before running `qpdf` (or `derect.sh`).
* `derect.sh`: remove rectangles such as backgrounds from a PDF.
* `streamed.py`: interactively remove text strings from a PDF, optionally
  learning a substitution cypher while doing so.
