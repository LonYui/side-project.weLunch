from unittest import TestCase

import cluster


class Test(TestCase):
    def test_get_userMale(self):
        tar = cluster.Male(userId = "123").save()
        result = cluster.getUser("123")
        self.assertTrue(result)
        tar.delete()
    def test_get_userFemale(self):
        tar = cluster.Female(userId = "234").save()
        result = cluster.getUser("234")
        self.assertTrue(result)
        tar.delete()
    def test_get_userfail(self):
        result = cluster.getUser("123")
        self.assertFalse(result)


