// this follows the order of definition in python/AnaList.py
TString GetSRName(Int_t fID, bool shapeRegions=false){

    if (!shapeRegions){
        switch(fID) { //cut&count names
            case 1:
                return "2jm"; break;
            case 2: 
                return "2jt"; break; 
            case 3: 
                return "2jW"; break;
            case 4:
                return "2jl"; break; 
            case 5: 
                return "3j"; break;
            case 6:
                return "4jl"; break;
            case 7: 
                return "4jW"; break; 
            case 8: 
                return "4jm"; break; 
            case 9: 
                return "4jt"; break; 
            case 10: 
                return "4jl-"; break; 
            case 11: 
                return "5j"; break; 
            case 12: 
                return "6jm"; break; 
            case 13: 
                return "6jt"; break; 
            case 14:
                return "6jt+"; break;
            case 15: 
               return "6jl"; break;
            case 16: 
               return "2jvt"; break;
            case 17: 
                return "4jAp"; break;  
            default: 
                return ""; break; 
        }
    } else { //shape fit names
        switch(fID) { 
            case 1: 
                return "2jv"; break; 
            case 2: 
                return "2jl"; break; 
            case 3: 
                return "2jm"; break; 
            case 4: 
                return "3jm"; break; 
            case 5: 
                return "3jt"; break; 
            case 6: 
                return "4jl"; break; 
            case 7: 
                return "4jm"; break; 
            case 8: 
                return "5jm"; break; 
            case 9: 
                return "5jt"; break; 
            case 10: 
                return "6jl"; break; 
            case 11: 
                return "6jm"; break; 
            case 12: 
                return "6jt"; break; 
            default: 
                return ""; break; 
        }

    }

    return "";
}
