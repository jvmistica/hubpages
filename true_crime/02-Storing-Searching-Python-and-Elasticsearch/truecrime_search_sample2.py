from elastic import es_search


result = es_search(story="arrested")
for ndx, val in enumerate(result):
    print("\n----------\n")
    print("Story", ndx + 1, "of", val.get("total"))
    print("Subject:", val.get("subject"))
