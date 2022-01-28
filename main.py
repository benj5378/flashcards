import json
import math
import os
import sys
from pathlib import Path

print(sys.argv)

width = 59.4
height = 35
pagewidth = 297
pageheight = 210

p = sys.argv[1]
f = open(p)
data = json.load(f)

f.close()


def createsvg(content, j):
    svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <svg
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:cc="http://creativecommons.org/ns#"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:svg="http://www.w3.org/2000/svg"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
        xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
        sodipodi:docname="temp.svg"
        inkscape:version="1.0 (4035a4fb49, 2020-05-01)"
        id="svg8"
        version="1.1"
        viewBox="0 0 {} {}"
        width="{}mm"
        height="{}mm">
        <defs
            id="defs2" />
        <sodipodi:namedview
            inkscape:document-units="mm"
            borderopacity="1.0"
            bordercolor="#666666"
            pagecolor="#ffffff"
            id="base" />
        <metadata
            id="metadata5">
            <rdf:RDF>
            <cc:Work
                rdf:about="">
                <dc:format>image/svg+xml</dc:format>
                <dc:type
                rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
                <dc:title></dc:title>
            </cc:Work>
            </rdf:RDF>
        </metadata>
        <g
            id="layer1"
            inkscape:groupmode="layer"
            inkscape:label="Layer 1">
        """.format(
        pagewidth, pageheight, pagewidth, pageheight
    )
    svg += content
    svg += """
    </g>
    </svg>"""
    output = open("./output{}.svg".format(j), "w")
    output.write(svg)
    output.close()


numberx = math.floor(pagewidth / width)
numbery = math.floor(pageheight / height)

num_pages = 0
num_current_card = 0


while num_current_card < len(data):
    for j in range(0, 2):
        svgcontents = ""
        if j == 0:
            initial = num_current_card
            i = num_current_card
        else:
            num_current_card = i
            i = initial

        stop = False

        for it_y in range(0, numbery):
            for it_x in range(0, numberx):
                x = it_x * width
                y = it_y * height
                x2 = x + width
                y2 = y + height
                textx = x + width / 2
                texty = y + 5
                print("i=", i, ", j=", j, ", len=", len(data))
                textcontent = data[i][j]
                fontsize = 3.5
                inlinesize = width - 5

                if j == 1:
                    x = pagewidth - it_x * width
                    x2 = x - width
                    textx = x - width / 2

                svgcontents += """
                    <g>
                        <path
                        d="M {},{} H {} V {} H {} Z"
                        style="fill:none;fill-opacity:0;stroke:#000000;stroke-width:0.2;stroke-linejoin:round;stroke-dashoffset:2.49449;stroke-opacity:1;paint-order:stroke markers fill;stroke-miterlimit:4;stroke-dasharray:none"
                        id="rect833" />
                        <text x="{}" y="{}" style="font-size: {}; inline-size: {}; font-family: 'Bodoni Moda'" dominant-baseline="hanging" text-anchor="middle">{}</text>
                    </g>""".format(
                    x, y, x2, y2, x, textx, texty, fontsize, inlinesize, textcontent
                )

                i += 1

                if i >= len(data) or i <= -1:
                    stop = True
                    print("??")
                    break

            createsvg(svgcontents, num_pages)

            if stop:
                break

        num_pages += 1
        print("cards left: ", num_current_card)
        print("initial: ", initial)
        print("here")


print(num_pages)

files = ""
for i in range(0, num_pages):
    os.system("inkscape output{}.svg --export-filename=output{}.pdf".format(i, i))
    files += "output{}.pdf ".format(i)
    print("page done: ", i)


filename = Path(p).stem
os.system("pdftk {}cat output {}.pdf".format(files, filename))
