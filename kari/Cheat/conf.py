keywords={
"g++":["int","long","short","switch","char","class","struct","for","while","if","else","break","continue","return","true","false","float","double","do","signed","unsigned"],
"gcc":["int","long","short","switch","char","struct","for","while","if","else","break","continue","return","float","double","do","signed","unsigned"],
"java":["int","long","short","switch","char","class","for","while","if","else","break","continue","return","float","double","do"]}


symbol={
"g++":["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"],
"gcc":["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"],
"java":["[","]","{","}","(",")","&","|","^","%","+","-","*","/",":",";","?","!",".","\"","\'",",","=","#","<",">","_","\\"]}

lang=["g++","gcc","java"]

rule = {"g++":"(\/\*(\s|.)*?\*\/)|(\/\/.*)",
        "gcc":"(\/\*(\s|.)*?\*\/)|(\/\/.*)",
        "java":"(\/\*(\s|.)*?\*\/)|(\/\/.*)"}
