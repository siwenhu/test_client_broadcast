#coding:utf-8

from xml.etree import ElementTree
import commands

def get_node_item(flag, xml, xpath):
    '''获取节点的文本 
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath:节点路径 '''
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    item = root.find(xpath)
    if item == None:
        return ""
    return item.text

def get_node_attrib(flag, xml, xpath, attrib):
    '''获取节点的属性 
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath:节点路径 
     attrib : 属性标签'''
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    return root.find(xpath).attrib[attrib]

def get_node_attrib_list(flag, xml, xpath, attrib):
    '''
    获取指定节点下所有的同名属性值
    @flag:True xml参数为文件； False xml参数为字符串
    @xml:xml文件名
    @xpath:节点路径
    @attrib：属性标签
    '''
    ret = []
    root = None
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    elements = root.findall(xpath)
    for e in elements:
        ret.append(e.attrib[attrib])
    return ret

def update_node_text(flag, xml, xpath, value):
    '''改变/增加/删除 节点的文本 
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath:节点路径 
     text : 更该后的文本'''
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    elements = root.findall(xpath)
    for e in elements:
        e.text = value
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")

def update_node_attrib(flag, xml, xpath, kv_map):
    '''修改/增加/删除 节点的属性及属性值
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath: 节点路径
     kv_map:属性及属性值map'''  
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    parent=root.findall(xpath)
    for node in parent:
        for key in kv_map:
            node.attrib[key]= kv_map.get(key)
    
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")
    
def del_node_attrib(flag, xml, xpath, key):
     
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    parent=root.findall(xpath)
    for node in parent:
        
        if node.attrib.has_key(key):
            node.attrib.pop(key)
    
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")

def update_node_attrib_val(flag, xml, xpath, key, old_val, new_val):
    '''
    更新指定节点的属性值
    @flag: True xml参数为文件； False xml参数为字符串
    @xml: xml文件名
    @xpath: 节点路径
    @old_val: 节点原来的值
    @new_avl: 节点的新值
    '''
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    parent=root.findall(xpath)
    for node in parent:
        if (old_val == node.attrib[key]):
            node.attrib[key] = new_val
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")

def del_node_by_attrib(flag, xml, xpath, tag, kv_map = None):  
    '''删除节点，通过属性及属性值定位这个节点
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath: 父节点路径
     tag:要删除的节点标签 
     kv_map: 属性及属性值列表''' 
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    prt=root.findall(xpath)
    for parent_node in prt:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag:
                if kv_map == None or if_match(child, kv_map):  
                    parent_node.remove(child)
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")
    
def del_node(flag, xml, xpath, tag, kv_map = None):  
    '''删除节点，通过属性及属性值定位这个节点
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath: 父节点路径
     tag:要删除的节点标签 
     kv_map: 属性及属性值列表''' 
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    prt=root.findall(xpath)
    for parent_node in prt:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag:
                if kv_map == None or if_match(child, kv_map):  
                    parent_node.remove(child)
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")
def del_a_node(flag, xml, xpath, tag):  
    
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    prt=root.findall(xpath)
    for parent_node in prt:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag:
                parent_node.remove(children)
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")

def del_parent_node_by_attrib(flag, xml, xpath, child_tag, kv_map = None):
    '''删除节点，通过属性及属性值定位这个节点
     @flag: True xml参数为文件； False xml参数为字符串
     @xml: xml文件名
     @xpath: 删除节点路径
     @child_tag: 要删除节点的子节点的节点标签 
     @kv_map: 属性及属性值列表'''
    if xpath.endswith('/'):
        xpath = xpath[:len(xpath)-1]
    nlist = xpath.split('/')
    length = len(nlist)
    if length < 2:
        return
    cur_tag = nlist[length-1]
    parent_tag = nlist[length-2]
    if flag:
        tree = ElementTree.ElementTree(file = xml)
    else:
        tree = ElementTree.fromstring(xml)
    for parent in tree.iter(tag=parent_tag):
        for cur in parent.iter(tag=cur_tag):
            is_matched = False
            for child in cur.getchildren():
                if child.tag == child_tag and if_match(child, kv_map):
                    is_matched = True
                    break
            if is_matched:
                parent.remove(cur)
                break
    if flag:
        tree.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(tree, encoding="utf-8")
    
def add_node(flag, xml, xpath, tag, attrib=None, text=None):  
    '''添加子节点 
     flag: True xml参数为文件； False xml参数为字符串
     xml: xml文件名
     xpath: 父节点路径 
     tag: 子节点tag
     attrib: 子节点属性
     text: 子节点文本'''
    if flag:
        root = ElementTree.ElementTree(file = xml)
    else:
        root = ElementTree.fromstring(xml)
    parent=root.findall(xpath)
    
    element = ElementTree.Element(tag=tag, attrib=attrib)
    element.text = text  
    node = parent[len(parent)-1]
    node.append(element)
    if flag:
        root.write(xml, encoding='utf-8')
    else:
        return ElementTree.tostring(root, encoding="utf-8")

def if_match(node, kv_map):  
    '''判断某个节点与参数属性是否相同
     node: 节点 
     kv_map: 属性及属性值组成的map'''  
    for key in kv_map:
        if node.get(key) != kv_map.get(key):  
            return False  
    return True

def img_get_backing(img):
    result = commands.getstatusoutput("qemu-img info " + img)  
    output = result[1]
    point = output.find("backing file: ")
    if point == -1:
        return None
    else:
        return output[point + len("backing file: "):]

# if __name__ == "__main__":
#     
#     del_parent_node_by_attrib(True, '/root/win_xp.xml', './devices/disk', 'source', {'file':'/var/lib/libvirt/images/win_xp_d.1'});
#     val = get_node_attrib(True, XML_PATH, './devices/disk/source', 'file')
#     
#     a = get_node_item(True, XML_PATH, './devices/emulator')
#     
#     nodelist = get_node_attrib_list(True, XML_PATH, './devices/input', 'type')
#     
#     update_node_text(True, XML_PATH, './devices/emulator','/usr/libexec/qemu-kvm')
    
