// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME SusyFitter_Dict

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// Since CINT ignores the std namespace, we need to do so in this file.
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "ChannelStyle.h"
#include "CombinationUtils.h"
#include "CombineWorkSpaces.h"
#include "ConfigMgr.h"
#include "DrawUtils.h"
#include "FitConfig.h"
#include "HypoTestTool.h"
#include "json.h"
#include "LimitResult.h"
#include "RooExpandedFitResult.h"
#include "RooHist.h"
#include "RooPlot.h"
#include "Significance.h"
#include "StatTools.h"
#include "TEasyFormula.h"
#include "TMsgLogger.h"
#include "toy_utils.h"
#include "Utils.h"
#include "ValidationUtils.h"
#include "XtraValues.h"

// Header files passed via #pragma extra_include

namespace Util {
   namespace ROOT {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *Util_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("Util", 0 /*version*/, "CombinationUtils.h", 33,
                     ::ROOT::DefineBehavior((void*)0,(void*)0),
                     &Util_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *Util_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace RooStats {
   namespace ROOT {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *RooStats_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("RooStats", 0 /*version*/, "CombineWorkSpaces.h", 37,
                     ::ROOT::DefineBehavior((void*)0,(void*)0),
                     &RooStats_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *RooStats_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace DrawUtil {
   namespace ROOT {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *DrawUtil_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("DrawUtil", 0 /*version*/, "DrawUtils.h", 24,
                     ::ROOT::DefineBehavior((void*)0,(void*)0),
                     &DrawUtil_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *DrawUtil_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace StatTools {
   namespace ROOT {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *StatTools_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("StatTools", 0 /*version*/, "Significance.h", 28,
                     ::ROOT::DefineBehavior((void*)0,(void*)0),
                     &StatTools_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *StatTools_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace ValidationUtils {
   namespace ROOT {
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance();
      static TClass *ValidationUtils_Dictionary();

      // Function generating the singleton type initializer
      inline ::ROOT::TGenericClassInfo *GenerateInitInstance()
      {
         static ::ROOT::TGenericClassInfo 
            instance("ValidationUtils", 0 /*version*/, "ValidationUtils.h", 41,
                     ::ROOT::DefineBehavior((void*)0,(void*)0),
                     &ValidationUtils_Dictionary, 0);
         return &instance;
      }
      // Insure that the inline function is _not_ optimized away by the compiler
      ::ROOT::TGenericClassInfo *(*_R__UNIQUE_(InitFunctionKeeper))() = &GenerateInitInstance;  
      // Static variable to force the class initialization
      static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstance(); R__UseDummy(_R__UNIQUE_(Init));

      // Dictionary for non-ClassDef classes
      static TClass *ValidationUtils_Dictionary() {
         return GenerateInitInstance()->GetClass();
      }

   }
}

namespace ROOT {
   static TClass *ConfigMgr_Dictionary();
   static void ConfigMgr_TClassManip(TClass*);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ConfigMgr*)
   {
      ::ConfigMgr *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::ConfigMgr));
      static ::ROOT::TGenericClassInfo 
         instance("ConfigMgr", "ConfigMgr.h", 36,
                  typeid(::ConfigMgr), DefineBehavior(ptr, ptr),
                  &ConfigMgr_Dictionary, isa_proxy, 0,
                  sizeof(::ConfigMgr) );
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ConfigMgr*)
   {
      return GenerateInitInstanceLocal((::ConfigMgr*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::ConfigMgr*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *ConfigMgr_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::ConfigMgr*)0x0)->GetClass();
      ConfigMgr_TClassManip(theClass);
   return theClass;
   }

   static void ConfigMgr_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *FitConfig_Dictionary();
   static void FitConfig_TClassManip(TClass*);
   static void *new_FitConfig(void *p = 0);
   static void *newArray_FitConfig(Long_t size, void *p);
   static void delete_FitConfig(void *p);
   static void deleteArray_FitConfig(void *p);
   static void destruct_FitConfig(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::FitConfig*)
   {
      ::FitConfig *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::FitConfig));
      static ::ROOT::TGenericClassInfo 
         instance("FitConfig", "FitConfig.h", 29,
                  typeid(::FitConfig), DefineBehavior(ptr, ptr),
                  &FitConfig_Dictionary, isa_proxy, 0,
                  sizeof(::FitConfig) );
      instance.SetNew(&new_FitConfig);
      instance.SetNewArray(&newArray_FitConfig);
      instance.SetDelete(&delete_FitConfig);
      instance.SetDeleteArray(&deleteArray_FitConfig);
      instance.SetDestructor(&destruct_FitConfig);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::FitConfig*)
   {
      return GenerateInitInstanceLocal((::FitConfig*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::FitConfig*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *FitConfig_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::FitConfig*)0x0)->GetClass();
      FitConfig_TClassManip(theClass);
   return theClass;
   }

   static void FitConfig_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static void delete_RooExpandedFitResult(void *p);
   static void deleteArray_RooExpandedFitResult(void *p);
   static void destruct_RooExpandedFitResult(void *p);
   static void streamer_RooExpandedFitResult(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooExpandedFitResult*)
   {
      ::RooExpandedFitResult *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::RooExpandedFitResult >(0);
      static ::ROOT::TGenericClassInfo 
         instance("RooExpandedFitResult", ::RooExpandedFitResult::Class_Version(), "RooExpandedFitResult.h", 29,
                  typeid(::RooExpandedFitResult), DefineBehavior(ptr, ptr),
                  &::RooExpandedFitResult::Dictionary, isa_proxy, 16,
                  sizeof(::RooExpandedFitResult) );
      instance.SetDelete(&delete_RooExpandedFitResult);
      instance.SetDeleteArray(&deleteArray_RooExpandedFitResult);
      instance.SetDestructor(&destruct_RooExpandedFitResult);
      instance.SetStreamerFunc(&streamer_RooExpandedFitResult);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooExpandedFitResult*)
   {
      return GenerateInitInstanceLocal((::RooExpandedFitResult*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::RooExpandedFitResult*)0x0); R__UseDummy(_R__UNIQUE_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_XtraValues(void *p = 0);
   static void *newArray_XtraValues(Long_t size, void *p);
   static void delete_XtraValues(void *p);
   static void deleteArray_XtraValues(void *p);
   static void destruct_XtraValues(void *p);
   static void streamer_XtraValues(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::XtraValues*)
   {
      ::XtraValues *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::XtraValues >(0);
      static ::ROOT::TGenericClassInfo 
         instance("XtraValues", ::XtraValues::Class_Version(), "XtraValues.h", 24,
                  typeid(::XtraValues), DefineBehavior(ptr, ptr),
                  &::XtraValues::Dictionary, isa_proxy, 16,
                  sizeof(::XtraValues) );
      instance.SetNew(&new_XtraValues);
      instance.SetNewArray(&newArray_XtraValues);
      instance.SetDelete(&delete_XtraValues);
      instance.SetDeleteArray(&deleteArray_XtraValues);
      instance.SetDestructor(&destruct_XtraValues);
      instance.SetStreamerFunc(&streamer_XtraValues);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::XtraValues*)
   {
      return GenerateInitInstanceLocal((::XtraValues*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::XtraValues*)0x0); R__UseDummy(_R__UNIQUE_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_TMsgLogger(void *p = 0);
   static void *newArray_TMsgLogger(Long_t size, void *p);
   static void delete_TMsgLogger(void *p);
   static void deleteArray_TMsgLogger(void *p);
   static void destruct_TMsgLogger(void *p);
   static void streamer_TMsgLogger(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TMsgLogger*)
   {
      ::TMsgLogger *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TMsgLogger >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TMsgLogger", ::TMsgLogger::Class_Version(), "TMsgLogger.h", 62,
                  typeid(::TMsgLogger), DefineBehavior(ptr, ptr),
                  &::TMsgLogger::Dictionary, isa_proxy, 16,
                  sizeof(::TMsgLogger) );
      instance.SetNew(&new_TMsgLogger);
      instance.SetNewArray(&newArray_TMsgLogger);
      instance.SetDelete(&delete_TMsgLogger);
      instance.SetDeleteArray(&deleteArray_TMsgLogger);
      instance.SetDestructor(&destruct_TMsgLogger);
      instance.SetStreamerFunc(&streamer_TMsgLogger);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TMsgLogger*)
   {
      return GenerateInitInstanceLocal((::TMsgLogger*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TMsgLogger*)0x0); R__UseDummy(_R__UNIQUE_(Init));
} // end of namespace ROOT

namespace ROOT {
   static void *new_ChannelStyle(void *p = 0);
   static void *newArray_ChannelStyle(Long_t size, void *p);
   static void delete_ChannelStyle(void *p);
   static void deleteArray_ChannelStyle(void *p);
   static void destruct_ChannelStyle(void *p);
   static void streamer_ChannelStyle(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::ChannelStyle*)
   {
      ::ChannelStyle *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::ChannelStyle >(0);
      static ::ROOT::TGenericClassInfo 
         instance("ChannelStyle", ::ChannelStyle::Class_Version(), "ChannelStyle.h", 27,
                  typeid(::ChannelStyle), DefineBehavior(ptr, ptr),
                  &::ChannelStyle::Dictionary, isa_proxy, 16,
                  sizeof(::ChannelStyle) );
      instance.SetNew(&new_ChannelStyle);
      instance.SetNewArray(&newArray_ChannelStyle);
      instance.SetDelete(&delete_ChannelStyle);
      instance.SetDeleteArray(&deleteArray_ChannelStyle);
      instance.SetDestructor(&destruct_ChannelStyle);
      instance.SetStreamerFunc(&streamer_ChannelStyle);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::ChannelStyle*)
   {
      return GenerateInitInstanceLocal((::ChannelStyle*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::ChannelStyle*)0x0); R__UseDummy(_R__UNIQUE_(Init));
} // end of namespace ROOT

namespace ROOT {
   static TClass *__gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_Dictionary();
   static void __gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_TClassManip(TClass*);
   static void *new___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p = 0);
   static void *newArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(Long_t size, void *p);
   static void delete___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p);
   static void deleteArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p);
   static void destruct___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)
   {
      ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> > *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >));
      static ::ROOT::TGenericClassInfo 
         instance("__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >", "string", 709,
                  typeid(::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >), DefineBehavior(ptr, ptr),
                  &__gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_Dictionary, isa_proxy, 0,
                  sizeof(::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >) );
      instance.SetNew(&new___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR);
      instance.SetNewArray(&newArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR);
      instance.SetDelete(&delete___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR);
      instance.SetDeleteArray(&deleteArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR);
      instance.SetDestructor(&destruct___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR);

      ::ROOT::AddClassAlternate("__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >","vector<ChannelStyle>::iterator");
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)
   {
      return GenerateInitInstanceLocal((::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *__gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)0x0)->GetClass();
      __gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_TClassManip(theClass);
   return theClass;
   }

   static void __gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static void *new_TEasyFormula(void *p = 0);
   static void *newArray_TEasyFormula(Long_t size, void *p);
   static void delete_TEasyFormula(void *p);
   static void deleteArray_TEasyFormula(void *p);
   static void destruct_TEasyFormula(void *p);
   static void streamer_TEasyFormula(TBuffer &buf, void *obj);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::TEasyFormula*)
   {
      ::TEasyFormula *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TInstrumentedIsAProxy< ::TEasyFormula >(0);
      static ::ROOT::TGenericClassInfo 
         instance("TEasyFormula", ::TEasyFormula::Class_Version(), "TEasyFormula.h", 29,
                  typeid(::TEasyFormula), DefineBehavior(ptr, ptr),
                  &::TEasyFormula::Dictionary, isa_proxy, 16,
                  sizeof(::TEasyFormula) );
      instance.SetNew(&new_TEasyFormula);
      instance.SetNewArray(&newArray_TEasyFormula);
      instance.SetDelete(&delete_TEasyFormula);
      instance.SetDeleteArray(&deleteArray_TEasyFormula);
      instance.SetDestructor(&destruct_TEasyFormula);
      instance.SetStreamerFunc(&streamer_TEasyFormula);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::TEasyFormula*)
   {
      return GenerateInitInstanceLocal((::TEasyFormula*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::TEasyFormula*)0x0); R__UseDummy(_R__UNIQUE_(Init));
} // end of namespace ROOT

namespace ROOT {
   static TClass *JSON_Dictionary();
   static void JSON_TClassManip(TClass*);
   static void *new_JSON(void *p = 0);
   static void *newArray_JSON(Long_t size, void *p);
   static void delete_JSON(void *p);
   static void deleteArray_JSON(void *p);
   static void destruct_JSON(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::JSON*)
   {
      ::JSON *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::JSON));
      static ::ROOT::TGenericClassInfo 
         instance("JSON", "json.h", 41,
                  typeid(::JSON), DefineBehavior(ptr, ptr),
                  &JSON_Dictionary, isa_proxy, 0,
                  sizeof(::JSON) );
      instance.SetNew(&new_JSON);
      instance.SetNewArray(&newArray_JSON);
      instance.SetDelete(&delete_JSON);
      instance.SetDeleteArray(&deleteArray_JSON);
      instance.SetDestructor(&destruct_JSON);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::JSON*)
   {
      return GenerateInitInstanceLocal((::JSON*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::JSON*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *JSON_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::JSON*)0x0)->GetClass();
      JSON_TClassManip(theClass);
   return theClass;
   }

   static void JSON_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *JSONException_Dictionary();
   static void JSONException_TClassManip(TClass*);
   static void delete_JSONException(void *p);
   static void deleteArray_JSONException(void *p);
   static void destruct_JSONException(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::JSONException*)
   {
      ::JSONException *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::JSONException));
      static ::ROOT::TGenericClassInfo 
         instance("JSONException", "json.h", 31,
                  typeid(::JSONException), DefineBehavior(ptr, ptr),
                  &JSONException_Dictionary, isa_proxy, 0,
                  sizeof(::JSONException) );
      instance.SetDelete(&delete_JSONException);
      instance.SetDeleteArray(&deleteArray_JSONException);
      instance.SetDestructor(&destruct_JSONException);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::JSONException*)
   {
      return GenerateInitInstanceLocal((::JSONException*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::JSONException*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *JSONException_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::JSONException*)0x0)->GetClass();
      JSONException_TClassManip(theClass);
   return theClass;
   }

   static void JSONException_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *RooStatscLcLHypoTestTool_Dictionary();
   static void RooStatscLcLHypoTestTool_TClassManip(TClass*);
   static void *new_RooStatscLcLHypoTestTool(void *p = 0);
   static void *newArray_RooStatscLcLHypoTestTool(Long_t size, void *p);
   static void delete_RooStatscLcLHypoTestTool(void *p);
   static void deleteArray_RooStatscLcLHypoTestTool(void *p);
   static void destruct_RooStatscLcLHypoTestTool(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::RooStats::HypoTestTool*)
   {
      ::RooStats::HypoTestTool *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::RooStats::HypoTestTool));
      static ::ROOT::TGenericClassInfo 
         instance("RooStats::HypoTestTool", "HypoTestTool.h", 45,
                  typeid(::RooStats::HypoTestTool), DefineBehavior(ptr, ptr),
                  &RooStatscLcLHypoTestTool_Dictionary, isa_proxy, 0,
                  sizeof(::RooStats::HypoTestTool) );
      instance.SetNew(&new_RooStatscLcLHypoTestTool);
      instance.SetNewArray(&newArray_RooStatscLcLHypoTestTool);
      instance.SetDelete(&delete_RooStatscLcLHypoTestTool);
      instance.SetDeleteArray(&deleteArray_RooStatscLcLHypoTestTool);
      instance.SetDestructor(&destruct_RooStatscLcLHypoTestTool);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::RooStats::HypoTestTool*)
   {
      return GenerateInitInstanceLocal((::RooStats::HypoTestTool*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::RooStats::HypoTestTool*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *RooStatscLcLHypoTestTool_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::RooStats::HypoTestTool*)0x0)->GetClass();
      RooStatscLcLHypoTestTool_TClassManip(theClass);
   return theClass;
   }

   static void RooStatscLcLHypoTestTool_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   static TClass *LimitResult_Dictionary();
   static void LimitResult_TClassManip(TClass*);
   static void *new_LimitResult(void *p = 0);
   static void *newArray_LimitResult(Long_t size, void *p);
   static void delete_LimitResult(void *p);
   static void deleteArray_LimitResult(void *p);
   static void destruct_LimitResult(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const ::LimitResult*)
   {
      ::LimitResult *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(::LimitResult));
      static ::ROOT::TGenericClassInfo 
         instance("LimitResult", "LimitResult.h", 26,
                  typeid(::LimitResult), DefineBehavior(ptr, ptr),
                  &LimitResult_Dictionary, isa_proxy, 0,
                  sizeof(::LimitResult) );
      instance.SetNew(&new_LimitResult);
      instance.SetNewArray(&newArray_LimitResult);
      instance.SetDelete(&delete_LimitResult);
      instance.SetDeleteArray(&deleteArray_LimitResult);
      instance.SetDestructor(&destruct_LimitResult);
      return &instance;
   }
   TGenericClassInfo *GenerateInitInstance(const ::LimitResult*)
   {
      return GenerateInitInstanceLocal((::LimitResult*)0);
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const ::LimitResult*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *LimitResult_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const ::LimitResult*)0x0)->GetClass();
      LimitResult_TClassManip(theClass);
   return theClass;
   }

   static void LimitResult_TClassManip(TClass* ){
   }

} // end of namespace ROOT

//______________________________________________________________________________
atomic_TClass_ptr RooExpandedFitResult::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *RooExpandedFitResult::Class_Name()
{
   return "RooExpandedFitResult";
}

//______________________________________________________________________________
const char *RooExpandedFitResult::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooExpandedFitResult*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int RooExpandedFitResult::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::RooExpandedFitResult*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *RooExpandedFitResult::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooExpandedFitResult*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *RooExpandedFitResult::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD2(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::RooExpandedFitResult*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr XtraValues::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *XtraValues::Class_Name()
{
   return "XtraValues";
}

//______________________________________________________________________________
const char *XtraValues::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::XtraValues*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int XtraValues::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::XtraValues*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *XtraValues::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::XtraValues*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *XtraValues::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD2(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::XtraValues*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TMsgLogger::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TMsgLogger::Class_Name()
{
   return "TMsgLogger";
}

//______________________________________________________________________________
const char *TMsgLogger::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TMsgLogger*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TMsgLogger::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TMsgLogger*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TMsgLogger::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TMsgLogger*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TMsgLogger::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD2(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TMsgLogger*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr ChannelStyle::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *ChannelStyle::Class_Name()
{
   return "ChannelStyle";
}

//______________________________________________________________________________
const char *ChannelStyle::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ChannelStyle*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int ChannelStyle::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::ChannelStyle*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *ChannelStyle::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ChannelStyle*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *ChannelStyle::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD2(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::ChannelStyle*)0x0)->GetClass(); }
   return fgIsA;
}

//______________________________________________________________________________
atomic_TClass_ptr TEasyFormula::fgIsA(0);  // static to hold class pointer

//______________________________________________________________________________
const char *TEasyFormula::Class_Name()
{
   return "TEasyFormula";
}

//______________________________________________________________________________
const char *TEasyFormula::ImplFileName()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TEasyFormula*)0x0)->GetImplFileName();
}

//______________________________________________________________________________
int TEasyFormula::ImplFileLine()
{
   return ::ROOT::GenerateInitInstanceLocal((const ::TEasyFormula*)0x0)->GetImplFileLine();
}

//______________________________________________________________________________
TClass *TEasyFormula::Dictionary()
{
   fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TEasyFormula*)0x0)->GetClass();
   return fgIsA;
}

//______________________________________________________________________________
TClass *TEasyFormula::Class()
{
   if (!fgIsA.load()) { R__LOCKGUARD2(gInterpreterMutex); fgIsA = ::ROOT::GenerateInitInstanceLocal((const ::TEasyFormula*)0x0)->GetClass(); }
   return fgIsA;
}

namespace ROOT {
} // end of namespace ROOT for class ::ConfigMgr

namespace ROOT {
   // Wrappers around operator new
   static void *new_FitConfig(void *p) {
      return  p ? new(p) ::FitConfig : new ::FitConfig;
   }
   static void *newArray_FitConfig(Long_t nElements, void *p) {
      return p ? new(p) ::FitConfig[nElements] : new ::FitConfig[nElements];
   }
   // Wrapper around operator delete
   static void delete_FitConfig(void *p) {
      delete ((::FitConfig*)p);
   }
   static void deleteArray_FitConfig(void *p) {
      delete [] ((::FitConfig*)p);
   }
   static void destruct_FitConfig(void *p) {
      typedef ::FitConfig current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::FitConfig

//______________________________________________________________________________
void RooExpandedFitResult::Streamer(TBuffer &R__b)
{
   // Stream an object of class RooExpandedFitResult.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      RooFitResult::Streamer(R__b);
      R__b.CheckByteCount(R__s, R__c, RooExpandedFitResult::IsA());
   } else {
      R__c = R__b.WriteVersion(RooExpandedFitResult::IsA(), kTRUE);
      RooFitResult::Streamer(R__b);
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrapper around operator delete
   static void delete_RooExpandedFitResult(void *p) {
      delete ((::RooExpandedFitResult*)p);
   }
   static void deleteArray_RooExpandedFitResult(void *p) {
      delete [] ((::RooExpandedFitResult*)p);
   }
   static void destruct_RooExpandedFitResult(void *p) {
      typedef ::RooExpandedFitResult current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_RooExpandedFitResult(TBuffer &buf, void *obj) {
      ((::RooExpandedFitResult*)obj)->::RooExpandedFitResult::Streamer(buf);
   }
} // end of namespace ROOT for class ::RooExpandedFitResult

//______________________________________________________________________________
void XtraValues::Streamer(TBuffer &R__b)
{
   // Stream an object of class XtraValues.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      {
         vector<double> &R__stl =  m_nObs;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<double> &R__stl =  m_nObs_eStat;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<double> &R__stl =  m_nPred;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<double> &R__stl =  m_nPred_eFit;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<double> &R__stl =  m_Delta;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<double> &R__stl =  m_Delta_eTot;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            double R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<TString> &R__stl =  m_reg_names;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            TString R__t;
            R__t.Streamer(R__b);
            R__stl.push_back(R__t);
         }
      }
      R__b.CheckByteCount(R__s, R__c, XtraValues::IsA());
   } else {
      R__c = R__b.WriteVersion(XtraValues::IsA(), kTRUE);
      {
         vector<double> &R__stl =  m_nObs;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<double> &R__stl =  m_nObs_eStat;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<double> &R__stl =  m_nPred;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<double> &R__stl =  m_nPred_eFit;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<double> &R__stl =  m_Delta;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<double> &R__stl =  m_Delta_eTot;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<double>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<TString> &R__stl =  m_reg_names;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<TString>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            ((TString&)(*R__k)).Streamer(R__b);
            }
         }
      }
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_XtraValues(void *p) {
      return  p ? new(p) ::XtraValues : new ::XtraValues;
   }
   static void *newArray_XtraValues(Long_t nElements, void *p) {
      return p ? new(p) ::XtraValues[nElements] : new ::XtraValues[nElements];
   }
   // Wrapper around operator delete
   static void delete_XtraValues(void *p) {
      delete ((::XtraValues*)p);
   }
   static void deleteArray_XtraValues(void *p) {
      delete [] ((::XtraValues*)p);
   }
   static void destruct_XtraValues(void *p) {
      typedef ::XtraValues current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_XtraValues(TBuffer &buf, void *obj) {
      ((::XtraValues*)obj)->::XtraValues::Streamer(buf);
   }
} // end of namespace ROOT for class ::XtraValues

//______________________________________________________________________________
void TMsgLogger::Streamer(TBuffer &R__b)
{
   // Stream an object of class TMsgLogger.

   TObject::Streamer(R__b);
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TMsgLogger(void *p) {
      return  p ? new(p) ::TMsgLogger : new ::TMsgLogger;
   }
   static void *newArray_TMsgLogger(Long_t nElements, void *p) {
      return p ? new(p) ::TMsgLogger[nElements] : new ::TMsgLogger[nElements];
   }
   // Wrapper around operator delete
   static void delete_TMsgLogger(void *p) {
      delete ((::TMsgLogger*)p);
   }
   static void deleteArray_TMsgLogger(void *p) {
      delete [] ((::TMsgLogger*)p);
   }
   static void destruct_TMsgLogger(void *p) {
      typedef ::TMsgLogger current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_TMsgLogger(TBuffer &buf, void *obj) {
      ((::TMsgLogger*)obj)->::TMsgLogger::Streamer(buf);
   }
} // end of namespace ROOT for class ::TMsgLogger

//______________________________________________________________________________
void ChannelStyle::Streamer(TBuffer &R__b)
{
   // Stream an object of class ChannelStyle.

   UInt_t R__s, R__c;
   if (R__b.IsReading()) {
      Version_t R__v = R__b.ReadVersion(&R__s, &R__c); if (R__v) { }
      TObject::Streamer(R__b);
      {
         vector<Int_t> &R__stl =  m_sampleColors;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            int R__t;
            R__b >> R__t;
            R__stl.push_back(R__t);
         }
      }
      {
         vector<TString> &R__stl =  m_sampleNames;
         R__stl.clear();
         int R__i, R__n;
         R__b >> R__n;
         R__stl.reserve(R__n);
         for (R__i = 0; R__i < R__n; R__i++) {
            TString R__t;
            R__t.Streamer(R__b);
            R__stl.push_back(R__t);
         }
      }
      m_logger.Streamer(R__b);
      m_name.Streamer(R__b);
      m_title.Streamer(R__b);
      R__b >> m_lumi;
      R__b >> m_dataColor;
      R__b >> m_totalPdfColor;
      R__b >> m_errorLineColor;
      R__b >> m_errorLineStyle;
      R__b >> m_errorFillColor;
      R__b >> m_errorFillStyle;
      R__b >> m_legend;
      R__b >> m_removeEmptyBins;
      R__b >> m_minY;
      R__b >> m_maxY;
      R__b >> m_nBins;
      m_titleX.Streamer(R__b);
      m_titleY.Streamer(R__b);
      R__b >> m_logY;
      R__b >> m_ATLASLabelX;
      R__b >> m_ATLASLabelY;
      m_ATLASLabelText.Streamer(R__b);
      R__b >> m_showLumi;
      R__b >> m_defaultSampleColor;
      R__b >> m_defaultSampleCounter;
      m_line1.Streamer(R__b);
      R__b >> m_textsize1;
      m_line2.Streamer(R__b);
      R__b >> m_textsize2;
      R__b.CheckByteCount(R__s, R__c, ChannelStyle::IsA());
   } else {
      R__c = R__b.WriteVersion(ChannelStyle::IsA(), kTRUE);
      TObject::Streamer(R__b);
      {
         vector<Int_t> &R__stl =  m_sampleColors;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<Int_t>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            R__b << (*R__k);
            }
         }
      }
      {
         vector<TString> &R__stl =  m_sampleNames;
         int R__n=int(R__stl.size());
         R__b << R__n;
         if(R__n) {
            vector<TString>::iterator R__k;
            for (R__k = R__stl.begin(); R__k != R__stl.end(); ++R__k) {
            ((TString&)(*R__k)).Streamer(R__b);
            }
         }
      }
      m_logger.Streamer(R__b);
      m_name.Streamer(R__b);
      m_title.Streamer(R__b);
      R__b << m_lumi;
      R__b << m_dataColor;
      R__b << m_totalPdfColor;
      R__b << m_errorLineColor;
      R__b << m_errorLineStyle;
      R__b << m_errorFillColor;
      R__b << m_errorFillStyle;
      R__b << m_legend;
      R__b << m_removeEmptyBins;
      R__b << m_minY;
      R__b << m_maxY;
      R__b << m_nBins;
      m_titleX.Streamer(R__b);
      m_titleY.Streamer(R__b);
      R__b << m_logY;
      R__b << m_ATLASLabelX;
      R__b << m_ATLASLabelY;
      m_ATLASLabelText.Streamer(R__b);
      R__b << m_showLumi;
      R__b << m_defaultSampleColor;
      R__b << m_defaultSampleCounter;
      m_line1.Streamer(R__b);
      R__b << m_textsize1;
      m_line2.Streamer(R__b);
      R__b << m_textsize2;
      R__b.SetByteCount(R__c, kTRUE);
   }
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_ChannelStyle(void *p) {
      return  p ? new(p) ::ChannelStyle : new ::ChannelStyle;
   }
   static void *newArray_ChannelStyle(Long_t nElements, void *p) {
      return p ? new(p) ::ChannelStyle[nElements] : new ::ChannelStyle[nElements];
   }
   // Wrapper around operator delete
   static void delete_ChannelStyle(void *p) {
      delete ((::ChannelStyle*)p);
   }
   static void deleteArray_ChannelStyle(void *p) {
      delete [] ((::ChannelStyle*)p);
   }
   static void destruct_ChannelStyle(void *p) {
      typedef ::ChannelStyle current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_ChannelStyle(TBuffer &buf, void *obj) {
      ((::ChannelStyle*)obj)->::ChannelStyle::Streamer(buf);
   }
} // end of namespace ROOT for class ::ChannelStyle

namespace ROOT {
   // Wrappers around operator new
   static void *new___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> > : new ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >;
   }
   static void *newArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >[nElements] : new ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >[nElements];
   }
   // Wrapper around operator delete
   static void delete___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p) {
      delete ((::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)p);
   }
   static void deleteArray___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p) {
      delete [] ((::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >*)p);
   }
   static void destruct___gnu_cxxcLcL__normal_iteratorlEChannelStylemUcOvectorlEChannelStylegRsPgR(void *p) {
      typedef ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> > current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >

//______________________________________________________________________________
void TEasyFormula::Streamer(TBuffer &R__b)
{
   // Stream an object of class TEasyFormula.

   TFormula::Streamer(R__b);
}

namespace ROOT {
   // Wrappers around operator new
   static void *new_TEasyFormula(void *p) {
      return  p ? new(p) ::TEasyFormula : new ::TEasyFormula;
   }
   static void *newArray_TEasyFormula(Long_t nElements, void *p) {
      return p ? new(p) ::TEasyFormula[nElements] : new ::TEasyFormula[nElements];
   }
   // Wrapper around operator delete
   static void delete_TEasyFormula(void *p) {
      delete ((::TEasyFormula*)p);
   }
   static void deleteArray_TEasyFormula(void *p) {
      delete [] ((::TEasyFormula*)p);
   }
   static void destruct_TEasyFormula(void *p) {
      typedef ::TEasyFormula current_t;
      ((current_t*)p)->~current_t();
   }
   // Wrapper around a custom streamer member function.
   static void streamer_TEasyFormula(TBuffer &buf, void *obj) {
      ((::TEasyFormula*)obj)->::TEasyFormula::Streamer(buf);
   }
} // end of namespace ROOT for class ::TEasyFormula

namespace ROOT {
   // Wrappers around operator new
   static void *new_JSON(void *p) {
      return  p ? new(p) ::JSON : new ::JSON;
   }
   static void *newArray_JSON(Long_t nElements, void *p) {
      return p ? new(p) ::JSON[nElements] : new ::JSON[nElements];
   }
   // Wrapper around operator delete
   static void delete_JSON(void *p) {
      delete ((::JSON*)p);
   }
   static void deleteArray_JSON(void *p) {
      delete [] ((::JSON*)p);
   }
   static void destruct_JSON(void *p) {
      typedef ::JSON current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::JSON

namespace ROOT {
   // Wrapper around operator delete
   static void delete_JSONException(void *p) {
      delete ((::JSONException*)p);
   }
   static void deleteArray_JSONException(void *p) {
      delete [] ((::JSONException*)p);
   }
   static void destruct_JSONException(void *p) {
      typedef ::JSONException current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::JSONException

namespace ROOT {
   // Wrappers around operator new
   static void *new_RooStatscLcLHypoTestTool(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) ::RooStats::HypoTestTool : new ::RooStats::HypoTestTool;
   }
   static void *newArray_RooStatscLcLHypoTestTool(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) ::RooStats::HypoTestTool[nElements] : new ::RooStats::HypoTestTool[nElements];
   }
   // Wrapper around operator delete
   static void delete_RooStatscLcLHypoTestTool(void *p) {
      delete ((::RooStats::HypoTestTool*)p);
   }
   static void deleteArray_RooStatscLcLHypoTestTool(void *p) {
      delete [] ((::RooStats::HypoTestTool*)p);
   }
   static void destruct_RooStatscLcLHypoTestTool(void *p) {
      typedef ::RooStats::HypoTestTool current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::RooStats::HypoTestTool

namespace ROOT {
   // Wrappers around operator new
   static void *new_LimitResult(void *p) {
      return  p ? new(p) ::LimitResult : new ::LimitResult;
   }
   static void *newArray_LimitResult(Long_t nElements, void *p) {
      return p ? new(p) ::LimitResult[nElements] : new ::LimitResult[nElements];
   }
   // Wrapper around operator delete
   static void delete_LimitResult(void *p) {
      delete ((::LimitResult*)p);
   }
   static void deleteArray_LimitResult(void *p) {
      delete [] ((::LimitResult*)p);
   }
   static void destruct_LimitResult(void *p) {
      typedef ::LimitResult current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class ::LimitResult

namespace ROOT {
   static TClass *vectorlEintgR_Dictionary();
   static void vectorlEintgR_TClassManip(TClass*);
   static void *new_vectorlEintgR(void *p = 0);
   static void *newArray_vectorlEintgR(Long_t size, void *p);
   static void delete_vectorlEintgR(void *p);
   static void deleteArray_vectorlEintgR(void *p);
   static void destruct_vectorlEintgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<int>*)
   {
      vector<int> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<int>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<int>", -2, "vector", 214,
                  typeid(vector<int>), DefineBehavior(ptr, ptr),
                  &vectorlEintgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<int>) );
      instance.SetNew(&new_vectorlEintgR);
      instance.SetNewArray(&newArray_vectorlEintgR);
      instance.SetDelete(&delete_vectorlEintgR);
      instance.SetDeleteArray(&deleteArray_vectorlEintgR);
      instance.SetDestructor(&destruct_vectorlEintgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<int> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<int>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEintgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<int>*)0x0)->GetClass();
      vectorlEintgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEintgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEintgR(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<int> : new vector<int>;
   }
   static void *newArray_vectorlEintgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<int>[nElements] : new vector<int>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEintgR(void *p) {
      delete ((vector<int>*)p);
   }
   static void deleteArray_vectorlEintgR(void *p) {
      delete [] ((vector<int>*)p);
   }
   static void destruct_vectorlEintgR(void *p) {
      typedef vector<int> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<int>

namespace ROOT {
   static TClass *vectorlEdoublegR_Dictionary();
   static void vectorlEdoublegR_TClassManip(TClass*);
   static void *new_vectorlEdoublegR(void *p = 0);
   static void *newArray_vectorlEdoublegR(Long_t size, void *p);
   static void delete_vectorlEdoublegR(void *p);
   static void deleteArray_vectorlEdoublegR(void *p);
   static void destruct_vectorlEdoublegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<double>*)
   {
      vector<double> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<double>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<double>", -2, "vector", 214,
                  typeid(vector<double>), DefineBehavior(ptr, ptr),
                  &vectorlEdoublegR_Dictionary, isa_proxy, 0,
                  sizeof(vector<double>) );
      instance.SetNew(&new_vectorlEdoublegR);
      instance.SetNewArray(&newArray_vectorlEdoublegR);
      instance.SetDelete(&delete_vectorlEdoublegR);
      instance.SetDeleteArray(&deleteArray_vectorlEdoublegR);
      instance.SetDestructor(&destruct_vectorlEdoublegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<double> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<double>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEdoublegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<double>*)0x0)->GetClass();
      vectorlEdoublegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEdoublegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEdoublegR(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<double> : new vector<double>;
   }
   static void *newArray_vectorlEdoublegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<double>[nElements] : new vector<double>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEdoublegR(void *p) {
      delete ((vector<double>*)p);
   }
   static void deleteArray_vectorlEdoublegR(void *p) {
      delete [] ((vector<double>*)p);
   }
   static void destruct_vectorlEdoublegR(void *p) {
      typedef vector<double> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<double>

namespace ROOT {
   static TClass *vectorlETStringgR_Dictionary();
   static void vectorlETStringgR_TClassManip(TClass*);
   static void *new_vectorlETStringgR(void *p = 0);
   static void *newArray_vectorlETStringgR(Long_t size, void *p);
   static void delete_vectorlETStringgR(void *p);
   static void deleteArray_vectorlETStringgR(void *p);
   static void destruct_vectorlETStringgR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<TString>*)
   {
      vector<TString> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<TString>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<TString>", -2, "vector", 214,
                  typeid(vector<TString>), DefineBehavior(ptr, ptr),
                  &vectorlETStringgR_Dictionary, isa_proxy, 0,
                  sizeof(vector<TString>) );
      instance.SetNew(&new_vectorlETStringgR);
      instance.SetNewArray(&newArray_vectorlETStringgR);
      instance.SetDelete(&delete_vectorlETStringgR);
      instance.SetDeleteArray(&deleteArray_vectorlETStringgR);
      instance.SetDestructor(&destruct_vectorlETStringgR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<TString> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<TString>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlETStringgR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<TString>*)0x0)->GetClass();
      vectorlETStringgR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlETStringgR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlETStringgR(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<TString> : new vector<TString>;
   }
   static void *newArray_vectorlETStringgR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<TString>[nElements] : new vector<TString>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlETStringgR(void *p) {
      delete ((vector<TString>*)p);
   }
   static void deleteArray_vectorlETStringgR(void *p) {
      delete [] ((vector<TString>*)p);
   }
   static void destruct_vectorlETStringgR(void *p) {
      typedef vector<TString> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<TString>

namespace ROOT {
   static TClass *vectorlEChannelStylegR_Dictionary();
   static void vectorlEChannelStylegR_TClassManip(TClass*);
   static void *new_vectorlEChannelStylegR(void *p = 0);
   static void *newArray_vectorlEChannelStylegR(Long_t size, void *p);
   static void delete_vectorlEChannelStylegR(void *p);
   static void deleteArray_vectorlEChannelStylegR(void *p);
   static void destruct_vectorlEChannelStylegR(void *p);

   // Function generating the singleton type initializer
   static TGenericClassInfo *GenerateInitInstanceLocal(const vector<ChannelStyle>*)
   {
      vector<ChannelStyle> *ptr = 0;
      static ::TVirtualIsAProxy* isa_proxy = new ::TIsAProxy(typeid(vector<ChannelStyle>));
      static ::ROOT::TGenericClassInfo 
         instance("vector<ChannelStyle>", -2, "vector", 214,
                  typeid(vector<ChannelStyle>), DefineBehavior(ptr, ptr),
                  &vectorlEChannelStylegR_Dictionary, isa_proxy, 4,
                  sizeof(vector<ChannelStyle>) );
      instance.SetNew(&new_vectorlEChannelStylegR);
      instance.SetNewArray(&newArray_vectorlEChannelStylegR);
      instance.SetDelete(&delete_vectorlEChannelStylegR);
      instance.SetDeleteArray(&deleteArray_vectorlEChannelStylegR);
      instance.SetDestructor(&destruct_vectorlEChannelStylegR);
      instance.AdoptCollectionProxyInfo(TCollectionProxyInfo::Generate(TCollectionProxyInfo::Pushback< vector<ChannelStyle> >()));
      return &instance;
   }
   // Static variable to force the class initialization
   static ::ROOT::TGenericClassInfo *_R__UNIQUE_(Init) = GenerateInitInstanceLocal((const vector<ChannelStyle>*)0x0); R__UseDummy(_R__UNIQUE_(Init));

   // Dictionary for non-ClassDef classes
   static TClass *vectorlEChannelStylegR_Dictionary() {
      TClass* theClass =::ROOT::GenerateInitInstanceLocal((const vector<ChannelStyle>*)0x0)->GetClass();
      vectorlEChannelStylegR_TClassManip(theClass);
   return theClass;
   }

   static void vectorlEChannelStylegR_TClassManip(TClass* ){
   }

} // end of namespace ROOT

namespace ROOT {
   // Wrappers around operator new
   static void *new_vectorlEChannelStylegR(void *p) {
      return  p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<ChannelStyle> : new vector<ChannelStyle>;
   }
   static void *newArray_vectorlEChannelStylegR(Long_t nElements, void *p) {
      return p ? ::new((::ROOT::TOperatorNewHelper*)p) vector<ChannelStyle>[nElements] : new vector<ChannelStyle>[nElements];
   }
   // Wrapper around operator delete
   static void delete_vectorlEChannelStylegR(void *p) {
      delete ((vector<ChannelStyle>*)p);
   }
   static void deleteArray_vectorlEChannelStylegR(void *p) {
      delete [] ((vector<ChannelStyle>*)p);
   }
   static void destruct_vectorlEChannelStylegR(void *p) {
      typedef vector<ChannelStyle> current_t;
      ((current_t*)p)->~current_t();
   }
} // end of namespace ROOT for class vector<ChannelStyle>

namespace {
  void TriggerDictionaryInitialization_libSusyFitter_Impl() {
    static const char* headers[] = {
"ChannelStyle.h",
"CombinationUtils.h",
"CombineWorkSpaces.h",
"ConfigMgr.h",
"DrawUtils.h",
"FitConfig.h",
"HypoTestTool.h",
"json.h",
"LimitResult.h",
"RooExpandedFitResult.h",
"RooHist.h",
"RooPlot.h",
"Significance.h",
"StatTools.h",
"TEasyFormula.h",
"TMsgLogger.h",
"toy_utils.h",
"Utils.h",
"ValidationUtils.h",
"XtraValues.h",
0
    };
    static const char* includePaths[] = {
"../include",
"/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/6.04.14-x86_64-slc6-gcc49-opt/include",
"/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/6.04.14-x86_64-slc6-gcc49-opt/include",
"/direct/usatlas+u/russsmith/testarea/zeroLeptonAnalysisHistFitter/ZeroLeptonAnalysis/HistFitterSetup/HistFitter-00-00-51/src/",
0
    };
    static const char* fwdDeclCode = 
R"DICTFWDDCLS(
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_Autoloading_Map;
class __attribute__((annotate("$clingAutoload$ConfigMgr.h")))  ConfigMgr;
class __attribute__((annotate("$clingAutoload$ConfigMgr.h")))  FitConfig;
class __attribute__((annotate(R"ATTRDUMP(Container class for expanded fit result)ATTRDUMP"))) __attribute__((annotate("$clingAutoload$RooExpandedFitResult.h")))  RooExpandedFitResult;
class __attribute__((annotate(R"ATTRDUMP(Container class)ATTRDUMP"))) __attribute__((annotate("$clingAutoload$ValidationUtils.h")))  XtraValues;
class __attribute__((annotate("$clingAutoload$ChannelStyle.h")))  TMsgLogger;
class __attribute__((annotate("$clingAutoload$ChannelStyle.h")))  ChannelStyle;
namespace std{template <typename _Tp> class __attribute__((annotate("$clingAutoload$string")))  allocator;
}
class __attribute__((annotate("$clingAutoload$TEasyFormula.h")))  TEasyFormula;
class __attribute__((annotate("$clingAutoload$json.h")))  JSON;
class __attribute__((annotate("$clingAutoload$json.h")))  JSONException;
namespace RooStats{class __attribute__((annotate("$clingAutoload$HypoTestTool.h")))  HypoTestTool;}
class __attribute__((annotate("$clingAutoload$LimitResult.h")))  LimitResult;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(

#ifndef G__VECTOR_HAS_CLASS_ITERATOR
  #define G__VECTOR_HAS_CLASS_ITERATOR 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
#include "ChannelStyle.h"
#include "CombinationUtils.h"
#include "CombineWorkSpaces.h"
#include "ConfigMgr.h"
#include "DrawUtils.h"
#include "FitConfig.h"
#include "HypoTestTool.h"
#include "json.h"
#include "LimitResult.h"
#include "RooExpandedFitResult.h"
#include "RooHist.h"
#include "RooPlot.h"
#include "Significance.h"
#include "StatTools.h"
#include "TEasyFormula.h"
#include "TMsgLogger.h"
#include "toy_utils.h"
#include "Utils.h"
#include "ValidationUtils.h"
#include "XtraValues.h"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[]={
"ChannelStyle", payloadCode, "@",
"CollectAndWriteHypoTestResults", payloadCode, "@",
"CollectAndWriteResultSet", payloadCode, "@",
"CollectHypoTestResults", payloadCode, "@",
"CollectLimitResults", payloadCode, "@",
"CollectWorkspaces", payloadCode, "@",
"ConfigMgr", payloadCode, "@",
"DrawUtil::linearsmooth", payloadCode, "@",
"DrawUtil::makesignificancehistos", payloadCode, "@",
"DrawUtil::triwsmooth", payloadCode, "@",
"FitConfig", payloadCode, "@",
"GetFitResultFromFile", payloadCode, "@",
"GetHypoTestResultFromFile", payloadCode, "@",
"GetMCStudy", payloadCode, "@",
"GetMatchingWorkspaces", payloadCode, "@",
"GetWorkspaceFromFile", payloadCode, "@",
"JSON", payloadCode, "@",
"JSONException", payloadCode, "@",
"LimitResult", payloadCode, "@",
"ParseWorkspaceID", payloadCode, "@",
"RooExpandedFitResult", payloadCode, "@",
"RooStats::AnalyzeHypoTestInverterResult", payloadCode, "@",
"RooStats::DoHypoTest", payloadCode, "@",
"RooStats::DoHypoTestInversion", payloadCode, "@",
"RooStats::HypoTestTool", payloadCode, "@",
"RooStats::get_Presult", payloadCode, "@",
"RooStats::get_Pvalue", payloadCode, "@",
"RooStats::get_htr", payloadCode, "@",
"RooStats::toyMC_gen_fit", payloadCode, "@",
"StatTools::DmLogL_PA", payloadCode, "@",
"StatTools::FindS95", payloadCode, "@",
"StatTools::FindSNSigma", payloadCode, "@",
"StatTools::FindXS95", payloadCode, "@",
"StatTools::FindXSNSigma", payloadCode, "@",
"StatTools::GetDLL", payloadCode, "@",
"StatTools::GetProbFromSigma", payloadCode, "@",
"StatTools::GetSigma", payloadCode, "@",
"StatTools::GetSimpleP1", payloadCode, "@",
"TEasyFormula", payloadCode, "@",
"TMsgLogger", payloadCode, "@",
"Util::GetToyMC", payloadCode, "@",
"ValidationUtils::PullPlot3", payloadCode, "@",
"WriteResultSet", payloadCode, "@",
"XtraValues", payloadCode, "@",
"__gnu_cxx::__normal_iterator<ChannelStyle*,vector<ChannelStyle> >", payloadCode, "@",
"clearVec", payloadCode, "@",
"get_Pvalue", payloadCode, "@",
"resetFloatPars", payloadCode, "@",
"vector<ChannelStyle>::iterator", payloadCode, "@",
nullptr};

    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("libSusyFitter",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_libSusyFitter_Impl, {}, classesHeaders);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_libSusyFitter_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_libSusyFitter() {
  TriggerDictionaryInitialization_libSusyFitter_Impl();
}
