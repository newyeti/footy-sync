# import unittest
# from loguru import logger
# from app.api.dependencies.api_key import ApiKeyService

# class TestApiKeyService(unittest.TestCase):
    
#     def setUp(self) -> ApiKeyService:
#         keys = ("first", "second", "thrid", "fourth")
#         self.daily_limit = 10
#         self.service = ApiKeyService(api_keys=keys, daily_limit=self.daily_limit)

#     def use_key_till_exaust(self):
#         for i in range(0, 10):
#             self.service.getKey(i+1)
            
#     def test_get_first_key(self):
#         current_key = self.service.getKey(0)
#         assert current_key.data.key == "first"
#         assert current_key.data.count == 0
        
#     def test_get_second_key(self):
#         self.use_key_till_exaust()
#         current_key = self.service.getKey(1)
#         assert current_key.data.key == "second"
    
#     def test_get_last_key(self):
#         for _ in range(0, 3):
#             self.use_key_till_exaust()
        
#         current_key = self.service.getKey(1)
            
#         assert current_key.data.key == "fourth"
    
#     def test_exaust_all_keys(self):
#         for i in range(0, 4):
#             self.use_key_till_exaust()
#         current_key = self.service.getKey(1)
#         assert current_key == None

# if __name__ == '__main__':
#     unittest.main()
    
