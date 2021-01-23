# -*- coding: utf-8 -*-

import datetime

import unittest

import tfl

vpc_tf='''resource "aws_vpc" "msk_vpc" {
  cidr_block = var.vpc_cidr
  tags = merge(
    local.common-tags,
    map(
      "Name", "msk-${lower(var.environment)}-vpc",
      "Description", "VPC for creating MSK resources",
    )
  )
}

resource "aws_vpc" "msk_vpc2" {
  cidr_block = var.vpc_cidr2
  tags = merge(
    local.common-tags,
    map(
      "Name", "msk-${lower(var.environment)}-vpc",
      "Description", "VPC for creating MSK resources",
    )
  )
}'''

def str2lines(s):
    return s.split('\n')

class TestHelper(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testXXX(self):
        ...
        lines = str2lines(vpc_tf)
        tfinst = tfl.TerraformFile('vpc.tf', lines)
        tfinsts = [tfinst]
        use_target = False
        tfl.output(tfinsts, use_target)

if __name__ == '__main__':
    unittest.main()
