from config import index
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, Boolean, Long, Date
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Post(Document):
    id = Long()
    tags = Keyword()
    blog_name = Keyword()
    liked = Boolean()
    format = Keyword()
    type = Keyword()
    caption = Text()
    slug = Keyword()
    # liked_timestamp = Date(format="epoch_second")
    # Temporarily saving as Long since format option isn't supported
    liked_timestamp = Long()
    date = Date()

    # class Meta:
    #     doc_type = "_doc"
    class Index:
        name = index
        
        settings = {
          "number_of_shards": 3,
        }
# Post.init()
