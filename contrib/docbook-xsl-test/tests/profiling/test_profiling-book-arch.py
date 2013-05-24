#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os.path
from lxml import etree
import pytest

import conftest as conf


DIR=os.path.dirname(__file__)


class TestSingleProfilingBookProfileArch():
   """Tests book profiling with one @arch profiling parameter"""
   @classmethod
   def setup_class(cls):
      """ setup class (only once) and transform XML file
      """
      cls.profattr = {'profile.arch': "'foo'"}
      cls.xf = conf.XMLFile( os.path.join(DIR, "profiling-book.xml") )
      cls.xf.parse( conf.STYLESHEETS["profile"] )
      cls.result = cls.xf.transform( **cls.profattr )
      cls.ns = conf.namespaces()

   def test_roots_thesame(self):
      """Checks, if root element before and after profiling is the same
      """
      src = self.xf.xml.getroot()
      dest = self.result.getroot()
      assert src.tag == dest.tag

   def test_chapter(self):
      """Checks, if the correct amount of chapters are seen
      """
      dest = self.result.xpath("/book/part[@id='singleprof-arch']/chapter")
      assert len(dest) == 2
   
   def test_chapter_ids(self):
      """Checks if available chapter id's are the same
      """
      dest = self.result.xpath("/book/part[@id='singleprof-arch']/chapter/@id")
      src= self.xf.xml.xpath("/book/part[@id='singleprof-arch']/chapter[not(@arch!='foo')]/@id")
      assert src == dest
      
   def test_chapter_section(self):
      """Checks, if the correct amount of sect1 are seen
      """
      dest = self.result.xpath("//chapter[@id='cha.arch.foo']/sect1")
      assert len(dest) == 2

   def test_chapter_section_ids(self):
      """Checks if available sect1 id's are the same
      """
      dest = self.result.xpath("//chapter[@id='cha.arch.foo']/sect1/@id")
      src=self.xf.xml.xpath("//chapter[@id='cha.arch.foo']/sect1[not(@arch!='foo')]/@id")
      assert src == dest

   def test_inline(self):
      """Checks if correct string is seen
      """
      dest = self.result.xpath("string(//sect1[@id='sec.arch.3']/para)").split()
      dest = " ".join(dest)
      para = self.xf.xml.xpath("//sect1[@id='sec.arch.3']/para")[0]
      res=[]
      for i in para.xpath("node()[not(self::phrase[@arch!='foo'])]"):
         if hasattr(i, "text"):
            res.append(i.text)
         else:
            res.append(i.strip())
      src = " ".join(res)
      assert dest == src


# EOF