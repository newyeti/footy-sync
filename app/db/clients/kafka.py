from app.core.settings.infra import KafkaSettings
from aiokafka import AIOKafkaProducer, AIOKafkaClient

import certifi
import ssl

class KafkaClient:
    def __init__(self, settings: KafkaSettings) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.bootstrap_servers,
                                         sasl_plain_username=settings.username,
                                         sasl_plain_password=settings.password,
                                         client_id=settings.client_id,
                                         sasl_mechanism=settings.sasl_mechanism,
                                         security_protocol=settings.security_protocol,
                                         ssl_context=ssl.create_default_context(cafile=certifi.where())
                                         )
    
    async def is_connected(self) -> bool:
        try:
            await self.producer.start()
            return True
        except Exception as e:
            return False
        # finally:
        #     await self.producer.stop()
    
    