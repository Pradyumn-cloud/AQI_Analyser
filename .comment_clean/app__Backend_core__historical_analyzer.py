
from pathlib import Path 
import pandas as pd 
import numpy as np 
import matplotlib .pyplot as plt 
import seaborn as sns 


sns .set (style ="whitegrid")

class HistoricalAnalyzer :
    """
    Loads the project's data CSV and generates the same analysis & plots
    as your original analysis.py for a single city (no 7/14/30-day filtering).
    Constructor signature matches your existing code: HistoricalAnalyzer(csv_filepath, plots_dir=None)
    """

    def __init__ (self ,csv_filepath ,plots_dir :str =None ):
        """
        csv_filepath: path to data.csv relative to app/ (e.g. "data_analysis/Data/data.csv")
        plots_dir: directory to save generated plots (relative to app/). Default: "assets/plots"
        """
        self .csv_filepath =Path (csv_filepath )
        if plots_dir is None :
            self .plots_dir =Path ("assets")/"plots"
        else :
            self .plots_dir =Path (plots_dir )
        self .plots_dir .mkdir (parents =True ,exist_ok =True )
        self ._df =None 


        self .pollutants =[
        'PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2',
        'O3','Benzene','Toluene','Xylene'
        ]

    def load_df (self ):
        if self ._df is not None :
            return self ._df 

        if not self .csv_filepath .exists ():
            raise FileNotFoundError (f"CSV not found: {self .csv_filepath }")


        df =pd .read_csv (self .csv_filepath ,low_memory =False )


        if 'Datetime'not in df .columns and 'Date'in df .columns :
            df ['Datetime']=pd .to_datetime (df ['Date'],errors ='coerce')
            if 'Hour'in df .columns :
                df ['Datetime']+=pd .to_timedelta (df ['Hour'],unit ='h')
        else :
            df ['Datetime']=pd .to_datetime (df ['Datetime'],errors ='coerce')


        if 'City'not in df .columns and 'city'in df .columns :
            df ['City']=df ['city']


        for p in self .pollutants :
            if p in df .columns :
                df [p ]=pd .to_numeric (df [p ],errors ='coerce')

        self ._df =df 
        return self ._df 

    def _save_fig (self ,fig ,filename :str )->str :
        """
        Save matplotlib figure to plots_dir and return a relative path string
        relative to assets directory, e.g. "plots/city_yearly.png"
        """
        out_path =self .plots_dir /filename 
        fig .savefig (out_path ,dpi =180 ,bbox_inches ='tight')
        plt .close (fig )

        rel =Path ("plots")/filename 
        return str (rel )

    def generate_city_analysis (self ,city :str ):
        """
        Perform the same analysis as analysis.py for the given city.
        Returns dict:
            {
              'city': city,
              'yearly_path': 'plots/..png',
              'monthly_path': ...,
              'hourly_path': ...,
              'most_toxic_path': ...,
              'heatmap_path': ...,
              'peak_months': {...},
              'best_month': int,
              'worst_month': int,
              'avg_pollutants': {pollutant: avg_value, ...}
            }
        """
        city =str (city ).strip ()
        df =self .load_df ()


        city_df =df [df ['City'].str .lower ()==city .lower ()].copy ()if 'City'in df .columns else pd .DataFrame ()
        if city_df .empty and 'City'in df .columns :
            city_df =df [df ['City'].str .lower ().str .contains (city .lower (),na =False )].copy ()

        if city_df .empty :
            return None 


        city_df =city_df .sort_values ('Datetime').ffill ()


        if 'Year'not in city_df .columns :
            city_df ['Year']=city_df ['Datetime'].dt .year 
        yearly =city_df .groupby ('Year')[self .pollutants ].mean ()

        fig ,ax =plt .subplots (figsize =(12 ,6 ))
        sns .lineplot (data =yearly ,ax =ax )
        ax .set_title (f'Yearly Trend of Pollutants in {city .title ()}')
        ax .set_ylabel ('Average Concentration')
        yearly_path =self ._save_fig (fig ,f"{city }_yearly.png")


        if 'Month'not in city_df .columns :
            city_df ['Month']=city_df ['Datetime'].dt .month 
        monthly =city_df .groupby ('Month')[self .pollutants ].mean ()

        fig ,ax =plt .subplots (figsize =(12 ,6 ))
        sns .lineplot (data =monthly ,ax =ax )
        ax .set_title (f'Monthly Average Pollutants in {city .title ()}')
        monthly_path =self ._save_fig (fig ,f"{city }_monthly.png")


        with np .errstate (all ='ignore'):
            monthly_mean =monthly .mean (axis =1 )
            best_month =int (monthly_mean .idxmin ())if not monthly_mean .empty else None 
            worst_month =int (monthly_mean .idxmax ())if not monthly_mean .empty else None 


        if 'Hour'not in city_df .columns :
            city_df ['Hour']=city_df ['Datetime'].dt .hour 
        hourly =city_df .groupby ('Hour')[self .pollutants ].mean ()

        fig ,ax =plt .subplots (figsize =(12 ,6 ))
        sns .lineplot (data =hourly ,ax =ax )
        ax .set_title (f'Hourly Pollution Pattern in {city .title ()}')
        hourly_path =self ._save_fig (fig ,f"{city }_hourly.png")


        avg_pollutants =city_df [self .pollutants ].mean ().sort_values (ascending =False )

        fig ,ax =plt .subplots (figsize =(10 ,6 ))
        sns .barplot (x =avg_pollutants .index ,y =avg_pollutants .values ,ax =ax )
        plt .setp (ax .get_xticklabels (),rotation =45 ,ha ='right')
        ax .set_title (f'Most Toxic Pollutants in {city .title ()} (Average)')
        most_toxic_path =self ._save_fig (fig ,f"{city }_most_toxic.png")

        most_toxic_overall =avg_pollutants .index [0 ]if not avg_pollutants .empty else None 


        peak_months ={}
        for p in self .pollutants :
            if p in monthly .columns :
                try :
                    peak_months [p ]=int (monthly [p ].idxmax ())
                except Exception :
                    peak_months [p ]=None 


        corr_cols =[p for p in self .pollutants if p in city_df .columns ]
        heatmap_path =None 
        if len (corr_cols )>=2 :
            corr =city_df [corr_cols ].corr ()
            fig ,ax =plt .subplots (figsize =(10 ,8 ))
            sns .heatmap (corr ,annot =True ,cmap ='coolwarm',ax =ax ,fmt ='.2f')
            ax .set_title (f'Correlation between Pollutants in {city .title ()}')
            heatmap_path =self ._save_fig (fig ,f"{city }_heatmap.png")

        result ={
        'city':city ,
        'yearly_path':yearly_path ,
        'monthly_path':monthly_path ,
        'hourly_path':hourly_path ,
        'most_toxic_path':most_toxic_path ,
        'heatmap_path':heatmap_path ,
        'peak_months':peak_months ,
        'best_month':best_month ,
        'worst_month':worst_month ,
        'most_toxic_overall':str (most_toxic_overall )if most_toxic_overall is not None else None ,
        'avg_pollutants':avg_pollutants .fillna (0 ).to_dict ()
        }
        return result 