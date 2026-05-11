from modules.medical_rag import retrieve_medical_context


query = "What are symptoms of diabetes?"


results = retrieve_medical_context(query)


for i, doc in enumerate(results, 1):

    print(f"\nResult {i}")
    print(doc)