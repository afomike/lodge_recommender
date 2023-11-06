from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# load lodge similarity
with open(f'model\lodgesimilarity.pkl', 'rb') as f:
    similarity = pickle.load(f)
# Load the the proprocess dataframe 
new  = pd.read_csv('model\lodge_list.csv')

def recommend(House_Location,Price,Amenities,Property_type):
    index = new[(new['House_Location']==House_Location) & (new['Price']==Price) & (new['Amenities']==Amenities) & (new['Property_type']==Property_type)].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_lodges = []
    printed_names = set()
    for i in distances[1:10]:
        row_index = i[0]
        House_Location = new.iloc[row_index]['House_Location']
        Price = new.iloc[row_index]['Price']
        Amenities = new.iloc[row_index]['Amenities']
        Property_type = new.iloc[row_index]['Property_type']
        House_Image = new.iloc[row_index]['House_Image']
        Agent_no =str(new.iloc[row_index]['Agent_no'])
        if House_Location not in printed_names:
            printed_names.add(House_Location)

            recommended_lodges.append(
                {'House_Location': House_Location, 'Price': Price, 'Amenities': Amenities, 'Agent_no': '0' + Agent_no, 'House_Image':House_Image, 'Property_type':Property_type})
    return recommended_lodges
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return(render_template('index.html'))

    if request.method == 'POST':
        try:
            House_Location = request.form['House_Location']
            Price = int(request.form['Price'])
            Amenities = request.form['Amenities']
            Property_type = request.form['Property_type']
            # House_Location = "nnpc felele"
            # Price = 170000
            # Amenities = "water and electricity"
            # Property_type ="self contained"

            recommended_lodges = recommend(House_Location, Price, Amenities, Property_type)
            return render_template('index.html', recommended_lodges=recommended_lodges)
        except Exception as e:
            default_recommendation =recommend("nnpc felele",170000,"water and electricity","self contained")
            return render_template('index.html', result=default_recommendation, error_message=str(e))
if __name__ == '__main__':
    app.run(debug=True)
