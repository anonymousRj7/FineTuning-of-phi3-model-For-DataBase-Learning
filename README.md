# FineTuning-of-phi3-model-For-DataBase-Learning


# 1. Use the Synthetic data generation by generate the answer of question given  in format of expected output
1.After generating the answer i make it into the format of finetuning of phi3 model

2. Format is ["instruction","input", "output"]

3.Then i upload this dataset on hugging face 

4.Used unsloth for faster finetuning

# 2. Unsupervised Finetuning
1. Create a database and upload on hugging face

2. Then use unsloth and trainer function for fine tuning

3. Here we can also add MLM ( mask id i.e currently in code it is comment)

4. Generate the output in json format.

# 2. Convert the Unsupervised data into supervised 
1.In this first i combined the data of all table given in table.json and convert them into csv (i.e code is given in data_preprocessing.py)

2.Then give input as whole table/relationship informatin , some instruction text and some output text(i.e i learned the database)

3.Then follow the same procedure (3 and 4 of above approach)
