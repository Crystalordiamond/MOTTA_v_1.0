# encoding: utf-8

from translate import Translator
a = ['你好']
translator= Translator(to_lang="en")
translation = translator.translate(a[0])
print(translation)