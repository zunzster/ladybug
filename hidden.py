#-------------------------------------------------------------------------------
# Name:        hidden
# Purpose:     hide hidden.txt inside sermons.html
#
# Author:      PWilson
#
# Created:     08/08/2020
# Copyright:   (c) PWilson 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
    tokens = []

    def handle_starttag(self, tag, attrs):
        txt = self.get_starttag_text()
        self.tokens.append(txt)

    def handle_endtag(self, tag):
        self.tokens.append('</' + tag + '>')

    def handle_comment(self, comment):
        self.tokens.append('<!--' + comment + '-->')

    def handle_decl(self, decl):
        self.tokens.append('<!' + decl + '>')

    def handle_data(self, data):
        self.tokens.append(data)

def tokenize(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.tokens

def steganographify(html, hide, pre, post):
    input = tokenize(html)
    hide = hide.replace(' ', '')
    hide = hide.lower()
    hide_pos = 0
    output = ''
    for token in input:
        if token[0] != '<' and hide_pos < len(hide):
            token_out = ''
            token_ofs = 0
            while hide_pos < len(hide):
                # find char
                ch = hide[hide_pos]
                ch_pos = token.find(ch, token_ofs)
                if ch_pos == -1:
                    token_out += token[token_ofs:]
                    break
                token_out += token[token_ofs:ch_pos]
                token_out += pre + ch + post
                token_ofs = ch_pos +1
                hide_pos += 1
                if hide_pos == len(hide):
                    token_out += token[token_ofs:]
                    break
                # next word
                ch_pos = token.find(' ', token_ofs)
                if ch_pos == -1:
                    token_out += token[token_ofs:]
                    break
                token_out += token[token_ofs:ch_pos +1]
                token_ofs = ch_pos +1
            output += token_out
        else:
            output += token
    return output

def main():
    with open('hidden.txt', 'r') as file:
        hide = file.read()
    with open('sermons_orig.html', 'r') as file:
        html = file.read()
    sermon_pos = html.index('<div id="sermonTwo"')
    sermon_end = html.index('<div id="sermonThree"', sermon_pos)
    pre = html[:sermon_pos]
    sermon = html[sermon_pos:sermon_end]
    post = html[sermon_end:]
    sermon_out = steganographify(sermon, hide, '<i>', '</i>')
    html_out = pre + sermon_out + post
    with open('sermons.html', 'w') as file:
        file.write(html_out)
    sermon_out = steganographify(sermon, hide, '<b><i>', '</i></b>')
    html_out = pre + sermon_out + post
    with open('sermons_bold.html', 'w') as file:
        file.write(html_out)

if __name__ == '__main__':
    main()
