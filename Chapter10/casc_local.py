"""
    Blizzard 사의 에셋 파일 시스템 뷰어.
    https://wowdev.wiki/CASC
"""

import os
import sys
import PyQt6
from PyQt6.QtWidgets import ( QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout )
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class MainWindow( QWidget ):

    def __init__( self ):
        """ 생성자 """
        super().__init__()
        self.initializeUI()

    def initializeUI( self ):
        """ UI 초기화, 생성자에서 호출됨 """
        self.setMinimumSize( 640, 480 )
        self.setWindowTitle( "WoW CASC Browser" )

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow( self ):
        """ 메인윈도우의 내부 구성하기 """

        listfile = "e-books/community-listfile.txt"
        listfile = os.path.join( os.getcwd(), listfile )
        id_name_map = {}
        name_id_map = {}
        filenames = []
        line_count = 0
        with open( listfile, "r" ) as f:
            for l in f.readlines():
                (
                    i,
                    n
                ) = l.split( ";", 2 )
                
                #id_name_map[ int( i ) ] = n.strip()
                #name_id_map[ n.strip() ] = int( i )
                filenames.append( ( n.strip(), i ) )
                line_count += 1
                if ( line_count > 1000000 ):
                    #break
                    pass
    
        file_tree = { 'folders': {}, 'files': {} }
        for fn in filenames:
            path = fn[0].replace( "\\", "/" ).split( "/" )
            top  = file_tree
            for sub in path[:-1]:
                if sub not in top["folders"]:
                    top["folders"][sub] = { "folders": {}, "files": {} }
                top = top["folders"][sub]
            top["files"][ path[-1] ] = fn

        self.tree_widget = QTreeWidget()
        #tree_widget.setColumnCount( 2 )
        self.tree_widget.setHeaderLabels( ["Fruit Type", "Description"] )
        self.tree_widget.setColumnWidth( 0, 320 )
        self.tree_widget.setAlternatingRowColors( True )
        self.tree_widget.setSortingEnabled( True )
        self.tree_widget.header().setSortIndicator( 0, Qt.SortOrder.AscendingOrder )

        category_1 = QTreeWidgetItem( self.tree_widget, ["Root", "가상루트"] )

        for f in file_tree["folders"]:
            category_1_child = QTreeWidgetItem( [ f ] )
            category_1_child.setData( 0, Qt.ItemDataRole.UserRole, file_tree["folders"][f] )
            sub_tree = file_tree["folders"][f]
            if sub_tree is not None and len( sub_tree["folders"] ) > 0:
                child_node = QTreeWidgetItem( category_1_child, ["__dummy__"] )
                #child_node.setData( 0, Qt.ItemDataRole.UserRole, sub_tree )
                category_1_child.addChild( child_node )
            category_1.addChild( category_1_child )


        main_v_box = QVBoxLayout()
        main_v_box.addWidget( self.tree_widget )
        self.setLayout( main_v_box )

        self.tree_widget.itemClicked.connect( self.onItemClicked )
        self.tree_widget.itemExpanded.connect( self.onItemExpanded )
    
    def onItemClicked( self, item ):
        #item = self.tree_widget.currentItem()
        print( item.text( 0 ) )
        #print( item.childCount() )
        #data = item.data( 0, Qt.ItemDataRole.UserRole )
        #print( data )

    def onItemExpanded( self, item ):
        #item = self.tree_widget.currentItem()
        #print( item.text( 0 ) )
        children = item.takeChildren()
        if len( children ) == 1 and children[0].text( 0 ) == "__dummy__":
            data = item.data( 0, Qt.ItemDataRole.UserRole )

            folder_list = data["folders"].keys()
            print( folder_list )

            for f in data["folders"]:
                sub_tree = data["folders"][f]

                sub_node = QTreeWidgetItem( [ f ] )
                sub_node.setData( 0, Qt.ItemDataRole.UserRole, sub_tree )
                
                if sub_tree is not None and len( sub_tree["folders"] ) > 0:
                    child_node = QTreeWidgetItem( ["__dummy__"] )
                    child_node.setData( 0, Qt.ItemDataRole.UserRole, sub_tree )
                    sub_node.addChild( child_node )

                item.addChild( sub_node )
        else:
            item.addChildren( children )
        

if __name__ == '__main__':
    app         = QApplication( sys.argv )
    main_window = MainWindow()
    sys.exit( app.exec() )