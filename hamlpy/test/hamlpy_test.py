import unittest
from nose.tools import eq_, raises
from hamlpy import hamlpy

class HamlPyTest(unittest.TestCase):
    htmlValues = ( ('<h1></h1>', '%h1'),
                   ('<div></div>', '%div'),
                   ('<one><two><three>Hey there</three></two></one>', '%one\n  %two\n    %three Hey there'),
                   ('<gee><whiz>Wow this is cool!</whiz></gee>', '%gee\n  %whiz\n    Wow this is cool!'))
    
    def test_outputs_simply_html_properly(self):
        hamlParser = hamlpy.Compiler()
        for html, haml in self.htmlValues:
            result = hamlParser.process(haml)
            #ignore \n
            assert html == result.replace('\n', '')
        
    def test_applies_id_properly(self):
        haml = '%div#someId Some text'
        html = "<div id='someId'>Some text</div>"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        self.assertEqual(html, result.replace('\n', ''))
        
    def test_applies_class_properly(self):
        haml = '%div.someClass Some text'
        html = "<div class='someClass'>Some text</div>"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        self.assertEqual(html, result.replace('\n', ''))
        
    def test_applies_multiple_classes_properly(self):
        haml = '%div.someClass.anotherClass Some text'
        html = "<div class='someClass anotherClass'>Some text</div>"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        self.assertEqual(html, result.replace('\n', ''))

    def test_dictionaries_define_attributes(self):
        haml = "%html{'xmlns':'http://www.w3.org/1999/xhtml', 'xml:lang':'en', 'lang':'en'}"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        self.assertTrue("<html" in result)
        self.assertTrue("xmlns='http://www.w3.org/1999/xhtml'" in result)
        self.assertTrue("xml:lang='en'" in result)
        self.assertTrue("lang='en'" in result)
        self.assertTrue(result.endswith("></html>") or result.endswith("></html>\n"))
    
    def testDictionariesSupportArraysForId(self):
        haml = "%div{'id':('itemType', '5')}"
        html = "<div id='itemType_5'></div>"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        self.assertEqual(html, result.replace('\n', ''))
        
    def test_html_comments_rendered_properly(self):
        haml = '/ some comment'
        html = "<!-- some comment -->"
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        eq_(html, result.replace('\n', ''))
        
    def test_django_variables_on_tag_render_properly(self):
        haml = '%div= story.tease'
        html = '<div>{{ story.tease }}</div>'
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        eq_(html, result.replace('\n', ''))
    
    def test_stand_alone_django_variables_render(self):
        haml = '= story.tease'
        html = '{{ story.tease }}'
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        eq_(html, result.replace('\n', ''))
    
    def test_stand_alone_django_tags_render(self):
        haml = '- extends "something.html"'
        html = '{% extends "something.html" %}'
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        eq_(html, result.replace('\n', ''))
        
    def test_if_else_django_tags_render(self):
        haml = '- if something\n   %p hello\n- else\n   %p goodbye'
        html = '{% if something %}<p>hello</p>{% else %}<p>goodbye</p>{% endif %}'
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        eq_(html, result.replace('\n', ''))
    
    @raises(TypeError)   
    def test_throws_exception_when_trying_to_close_django(self):
        haml = '- endfor'
        hamlParser = hamlpy.Compiler()
        result = hamlParser.process(haml)
        
        
