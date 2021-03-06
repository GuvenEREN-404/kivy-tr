# -*- coding: utf-8 -*-

import os
import gettext
import sqlite3
import sqlite3 as lite
import sys

from functools import partial
#Icons are downloaded from http://icons.iconarchive.com, see licanses for individual icon.

TYPES=("INTEGER", "TEXT", "BOOLEAN", "NUMERIC", "BLOB")

gettext.bindtextdomain('kivysqlite', 'language')
 
 
from  kivy.lang import Builder

from kivy.app import App

from kivy.uix.popup import Popup 
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

def _(*args):
    return App.get_running_app().get_text(*args)
 
 
class fileOpenForm(Popup):
    pass 
 
 

class ConfirmPopup(Popup):
    def __init__(self,**kwargs):
        self.text= kwargs['text']
        self.register_event_type('on_answer')
        super(ConfirmPopup,self).__init__(**kwargs)
        self.text= kwargs['text']
        self.result=None
    
    def on_answer(self, *args):
        pass
    
 
 
class KivySQLiteApp(App):

    def build(self):
        self.recent_path=os.getcwd()
        self.cursor=None
        self.set_language('tr')
        self.table_to_delete=None
        return Builder.load_file('main.kv')
          
          
    def showError(self, text):
        content=Label(text=text, markup=True)
        popup = Popup(title='Warning !', content=content)
        popup.size_hint = (0.7,0.7)

        popup.open()

          
    def fileOpenDialog(self):
        form = fileOpenForm()
        form.open()


    def openDB(self, db_select):

        try: 
            conn = lite.connect(db_select.selection[0])
        except:
            self.showError(_("Error open db"))
            return

        self.cursor = conn.cursor()
        self.update_tables_tree()
        self.root.ids.new_table_action.disabled=False
       
       


    def argConverter(self, row, item):
        print item
        return {'text': item["name"], 'size_hint_y': None, 'height': 25} 
        
        
    def update_tables_tree(self):
    
        
    
        data=[]
    
        for typ in ('table','view'):
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type = '%s'" % typ)
            result=self.cursor.fetchall()
   
            if result:
                for tb in result:
                    data.append({'name':tb[0]})
                    

        self.root.ids.main_table_list.adapter.data=data
        print data
        
        
        """tvlabeltext='[ref=""]{0} ({1})[/ref]'.format( _(typ.title()+'s'), len(result) )
                tvlabel=TreeViewLabel(text=tvlabeltext, markup=True)
                
                tvlabel.bind(on_ref_press=self.table_select)
                parent_node=self.root.ids.table_tree.add_node(tvlabel)
                for tb in result:
                    tvlabeltext='[ref="{0}"]{0}[/ref]'.format(tb[0])
                    tvlabel=TreeViewLabel(text=tvlabeltext, markup=True)
                    tvlabel.tbtype=typ
                    tvlabel.tbname=tb[0]
                    tvlabel.bind(on_ref_press=self.table_select)
                    tb_node=self.root.ids.table_tree.add_node(tvlabel, parent_node)
                    
                    self.cursor.execute('PRAGMA TABLE_INFO(`%s`)' % tb[0])
                    
                    for field in self.cursor.fetchall():
                        tvlabeltext='[ref=""][b]{0}[/b]    {1}[/ref]'.format( field[1], field[2] )
                        tvlabel=TreeViewLabel(text=tvlabeltext, markup=True)
                        tvlabel.bind(on_ref_press=self.table_select)
                    
                        self.root.ids.table_tree.add_node(tvlabel, tb_node)

                   """ 
            
        
    def deleteTableDialog(self):
        tb=self.root.ids.table_tree.selected_node
        form = ConfirmPopup(text=_("All data in the table you selected will be deleted!\n Are you sure you want to delete table [b]%s[/b]?") % tb.text)

        form.bind(on_answer=self.delete_table)
        form.open()
        
        
    def table_select(self, *tb):

        if hasattr(tb[0],'tbtype'): 
            self.root.ids.delete_table_action.disabled=False
        else:
            self.root.ids.delete_table_action.disabled=True
        
    def tree_view_expanded(self):
        pass
        
    def delete_table(self, instance, answer):
        tb=self.root.ids.table_tree.selected_node
        if answer=='yes':
            try:
                self.cursor.execute('DROP TABLE `%s`' % tb.tbname)
            except Exception as error:
                self.showError(_("An error occurred while droping table.\nThe message returned by sqlite engine is:")+"\n"+str(error))
            
            self.update_tables_tree()
        
        instance.dismiss()
      
    def set_language(self,selectedLanguage):
        self.t = gettext.translation('kivysqlite', 'language', languages=[selectedLanguage], fallback=True)

 
    def get_text(self, *args):
        return self.t.ugettext(*args)
    

 
if __name__ == '__main__':
    KivySQLiteApp().run()
