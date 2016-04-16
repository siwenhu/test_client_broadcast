# -*- coding: utf-8 -*-

import ConfigParser
import common
import globalvariable
import globalfunc
from logrecord import LogRecord

class ConfigFileParser():
    _instance = 0
    def __init__(self):       
        self.conf = ConfigParser.ConfigParser()

        self.configFile = common.CONFIG_PATH

        if globalvariable.PROGRAM_RUNNING_TYPE == common.OPERATION_ENV_TYPE:
            self.conf.read(globalfunc.convertPathToConfigPath(common.CONFIG_PATH))
            self.configFile = globalfunc.convertPathToConfigPath(common.CONFIG_PATH)
        else:
            self.conf.read(common.CONFIG_PATH)


    @classmethod 
    def instance(cls):
        if (cls._instance == 0):
            cls._instance = ConfigFileParser()
            
        return cls._instance
    
    def getValue(self, section, option):
        """获取指定的section， 指定的option的值"""
        value = None
        if self.conf.has_section(section):
            if self.conf.has_option(section, option):
                value = self.conf.get(section, option)
        return value

    def addSection(self, new_section, option=None, value=None):
        """写入指定section, 增加新option的值"""
        if not self.conf.has_section(new_section):
            self.conf.add_section(new_section)
            #判断键值和数据是否有效
            if option and value:
                self.conf.set(new_section, option, value)
            fpw = open(self.configFile, "w") 
            self.conf.write(fpw)
            fpw.close()
            return True

        return False
    
    def addOption(self, section, option, value):
        """在指定的section, 增加新option的值"""
        if self.conf.has_section(section):
            if not self.conf.has_option(section, option):
                self.conf.set(section, option, value)
                fpw = open(self.configFile, "w") 
                self.conf.write(fpw)
                fpw.close()
                return True
        
        return False
            
    def has_section(self, section):
        """是否存在指定的section"""
        if self.conf.has_section(section):
            return True
        return False
    
    def has_option(self, section, option):
        """是否存在指定的option"""
        if self.conf.has_section(section):
            if self.conf.has_option(section, option):
                return True
        return False
        
    def options(self, section):
        """返回所有的option"""
        return self.conf.options(section);
    
    def sections(self):
        """返回所有的section"""
        return self.conf.sections()

        
    def changeSectionValue(self, section, option, value):
        """更新指定section, option的值"""  
        if self.conf.has_section(section):
            if self.conf.has_option(section, option):
                self.conf.set(section, option, value)
                fpw = open(self.configFile, "w") 
                self.conf.write(fpw)
                fpw.close()
                return True
            
        return False
    
    def remove_section(self, section):
        """删除指定的section"""
        if self.conf.has_section(section):
            self.conf.remove_section(section)
            fpw = open(self.configFile, "w") 
            self.conf.write(fpw)
            fpw.close()
            return True
        
        return False
    
    def remove_option(self, section, option):
        """删除指定的option"""
        if self.conf.has_section(section):
            if self.conf.has_option(section, option):
                self.conf.remove_option(section, option)
                self.conf.write(open(self.configFile,"w"))
                return True
            
        return False
    
    
        
        






        
