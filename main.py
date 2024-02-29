import json
import os
from langchain.tools.convert_to_openai import format_tool_to_openai_function
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http import models


from crew import CustomResearchCrew

def create_kwargs(**fields):
    """
    Function to dynamically create keyword arguments based on a dictionary of field names and values.
    """
    kwargs = {}
    for field, value in fields.items():
        if isinstance(value, bool):
            value = str(value)
        kwargs[field] = value
    return kwargs


def create_filter(**kwargs, type_filter : str):
    """
    Function to dynamically create a 'must' filter based on key-value pairs.
    """
    conditions = []
    for key, value in kwargs.items():
		value = MatchValue(value=value)
        must_conditions.append(
            FieldCondition(
                key=key,
                match=value
            )
        )
	if type_filter.lower() == 'must':
		return Filter(must=conditions)
	else if type_filter.lower() == 'should':
		return Filter(should=conditions)





# Setup OpenAI 
os.environ['OPENAI_API_KEY'] = "sk-**************************"

llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview", request_timeout=120, max_retries=3)
        
# Ask for json structure (obviously correct it and ensure output is right, this is just an example)  
# I.e: pass tools, use Agents etc.      
json_test_qdrant_search = llm.predict_messages([HumanMessage(content=
                                        """
                                        Produce JSON structure to research for only files that are being elaborated (.....)
                                        """)])


# Example output
# json_test_qdrant_search = """
# {
#   "is_done": false,
#   "is_elaborating": true
# }
# """


# Setup Qdrant
url = "https://qdrant-uri.test/test1"
qdrant_api_key = "*********************"

# Qdrant collection name
qdrant_coll_name = "my_coll_name"

client_qdrant = QdrantClient(url=url, api_key=qdrant_api_key, prefer_grpc=False)


#Clean null Nodes
json_obj_result = del_null_none_branch(json_test_qdrant_search)
print(f"Clean result %s" % (json_obj_result))


# Create args to pass to create dynamic Qdrant filter during runtime
kwargs = hfutils.create_kwargs(**json_obj_result)


# Create runtime Filter object
qdrant_scroll_filter_runtime=create_filter(**kwargs, 'must')

# Search with filter
result_db = client_qdrant.scroll(
    collection_name=qdrant_coll_name,
    scroll_filter=scroll_filter_hf
)

# Print total results
print("\n\n\Total results count: %s" % len(result_db[0]))


source_data_vect = ""

# Example extracting "file_path" data from Qdrant DB
if len(result_db[0]) > 0:
    for elab in result_db[0]:
        if elab is not None:
            if elab.payload is not None and elab.payload['file_path']:
                with open(elab.payload["path_template_atto"], 'r', encoding="utf-8", errors="ignore") as f:
                    source_data_vect += f.read()
					source_data_vect += "\n"
                    


print(f"\n\n\n\nFull source %s" % (source_data_vect))