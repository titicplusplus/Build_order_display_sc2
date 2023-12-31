
def export_bo_creator(data, filename):
    #print(data[0])
    #print([",".join(d) for d in data])
    #print("\n".join([",".join(d) for d in data]))
    with open("./config_bo/" + filename + ".csv", "w") as f:
        f.write("\n".join([",".join(d) for d in data]))
