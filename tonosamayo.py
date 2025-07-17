import React, { useState } from 'react';
import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Textarea } from './components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Label } from './components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Checkbox } from './components/ui/checkbox';
import { Badge } from './components/ui/badge';
import { Progress } from './components/ui/progress';
import { Separator } from './components/ui/separator';
import { 
  AlertCircle, CheckCircle, Upload, ArrowLeft, ArrowRight, Star, 
  Zap, Shield, Cpu, Mic, Crown, Sparkles, Globe, Gift
} from 'lucide-react';

// Types and interfaces
interface MenuData {
  id: number;
  name: string;
  price: string;
  category: string;
  order: number;
  imageUrl?: string;
  allergens: string[];
  multilingualDescriptions: Record<string, string>;
  isFeatured: boolean;
  shouldIntroduce: boolean;
}

interface OwnerAnswers {
  restaurant_name: string;
  years_in_business: string;
  location_features: string;
  concept: string;
  ingredient_commitment: string;
  service_approach: string;
  signature_dish: string;
  seasonal_menus: string;
  menu_development: string;
  international_experience: string;
  cultural_sharing: string;
  international_message: string;
  future_goals: string;
  multilingual_expectations: string;
  customer_message: string;
}

interface Plan {
  id: string;
  name: string;
  description: string;
  features: string[];
  recommended: boolean;
}

// Configuration constants
const CONFIG = {
  commonAllergens: [
    "小麦", "甲殻類", "卵", "魚", "大豆", "ピーナッツ", 
    "牛乳", "くるみ", "セロリ", "マスタード", "ゴマ", 
    "亜硫酸塩", "ルピナス", "貝"
  ],
  menuCategories: ["フード", "コース", "ランチ", "デザート", "ドリンク"],
  plans: [
    {
      id: "basic",
      name: "ベーシックプラン",
      description: "基本的な多言語メニュー作成",
      features: ["5言語対応", "基本メニュー翻訳", "CSVファイル出力"],
      recommended: false
    },
    {
      id: "premium",
      name: "プレミアムプラン",
      description: "高品質な多言語メニュー作成",
      features: ["15言語対応", "高品質翻訳", "イチオシメニュー設定", "画像対応", "CSVファイル出力"],
      recommended: true
    },
    {
      id: "enterprise",
      name: "エンタープライズプラン",
      description: "完全カスタマイズ可能",
      features: ["全言語対応", "AI翻訳", "完全カスタマイズ", "24時間サポート", "API連携"],
      recommended: false
    }
  ]
};

// Mock functions
const authenticateCredentials = async (storeId: string, memberNumber: string): Promise<boolean> => {
  await new Promise(resolve => setTimeout(resolve, 1000));
  return storeId === "TONOSAMA001" && memberNumber === "99999";
};

const performOCR = async (file: File): Promise<MenuData[]> => {
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  const mockMenus: MenuData[] = [
    {
      id: 1001,
      name: "唐揚げ定食",
      price: "980円",
      category: "フード",
      order: 0,
      allergens: ["小麦", "大豆"],
      multilingualDescriptions: { "日本語": "唐揚げ定食" },
      isFeatured: false,
      shouldIntroduce: true
    },
    {
      id: 1002,
      name: "焼き魚御膳",
      price: "1200円",
      category: "フード",
      order: 1,
      allergens: ["魚"],
      multilingualDescriptions: { "日本語": "焼き魚御膳" },
      isFeatured: false,
      shouldIntroduce: true
    },
    {
      id: 1003,
      name: "特製ラーメン",
      price: "850円",
      category: "フード",
      order: 2,
      allergens: ["小麦", "卵"],
      multilingualDescriptions: { "日本語": "特製ラーメン" },
      isFeatured: false,
      shouldIntroduce: true
    }
  ];
  
  return mockMenus;
};

export default function App() {
  // State management
  const [currentStep, setCurrentStep] = useState(0);
  const [selectedPlan, setSelectedPlan] = useState<string>("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [storeId, setStoreId] = useState("");
  const [memberNumber, setMemberNumber] = useState("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [menus, setMenus] = useState<MenuData[]>([]);
  const [ownerAnswers, setOwnerAnswers] = useState<OwnerAnswers>({
    restaurant_name: "",
    years_in_business: "",
    location_features: "",
    concept: "",
    ingredient_commitment: "",
    service_approach: "",
    signature_dish: "",
    seasonal_menus: "",
    menu_development: "",
    international_experience: "",
    cultural_sharing: "",
    international_message: "",
    future_goals: "",
    multilingual_expectations: "",
    customer_message: ""
  });
  const [allergyPolicy, setAllergyPolicy] = useState<"display" | "hide" | "disclaimer_only">("display");
  const [allergyDisclaimer, setAllergyDisclaimer] = useState("");
  const [featuredMenus, setFeaturedMenus] = useState<MenuData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isCompleted, setIsCompleted] = useState(false);

  const steps = ["プラン", "ログイン", "メニュー", "詳細設定", "店主の想い", "イチオシ", "完成！"];

  const updateAnswer = (key: keyof OwnerAnswers, value: string) => {
    setOwnerAnswers(prev => ({ ...prev, [key]: value }));
  };

  // Enhanced Navigation component
  const Navigation = () => (
    <div className="w-full max-w-7xl mx-auto mb-12">
      <div className="ps3-nav p-8">
        {/* Step indicators */}
        <div className="grid grid-cols-7 gap-4 mb-8">
          {steps.map((step, index) => (
            <div
              key={index}
              className={`relative transition-all duration-500 ${
                index === currentStep ? 'scale-110' : ''
              }`}
            >
              <div className={`ps3-step text-center p-4 ${
                index === currentStep ? 'active ps3-glow' : 
                index < currentStep ? 'bg-green-600/30 border-green-400/50' : ''
              }`}>
                <div className={`w-10 h-10 mx-auto mb-2 rounded-full flex items-center justify-center text-lg font-bold ${
                  index === currentStep ? 'bg-white text-blue-600' : 
                  index < currentStep ? 'bg-green-500 text-white' :
                  'bg-gray-600 text-gray-300'
                }`}>
                  {index < currentStep ? '✓' : index + 1}
                </div>
                <div className={`text-sm font-medium ${
                  index === currentStep ? 'text-white' : 
                  index < currentStep ? 'text-green-300' :
                  'text-gray-400'
                }`}>
                  {step}
                </div>
              </div>
              
              {/* Connection line */}
              {index < steps.length - 1 && (
                <div className={`absolute top-1/2 left-full w-4 h-0.5 -translate-y-1/2 ${
                  index < currentStep ? 'bg-green-400' : 'bg-gray-600'
                }`} />
              )}
            </div>
          ))}
        </div>
        
        {/* Progress bar */}
        <div className="space-y-4">
          <div className="ps3-progress h-4 relative">
            <div 
              className="ps3-progress-bar h-full transition-all duration-1000 ease-out"
              style={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
            />
          </div>
          <div className="flex justify-between text-sm text-gray-300">
            <span>進捗状況</span>
            <span className="font-bold text-blue-300">
              {Math.round((currentStep / (steps.length - 1)) * 100)}% 完了
            </span>
          </div>
          <p className="text-center text-lg text-blue-300 font-medium">
            {currentStep === 0 && "プランを選択してください"}
            {currentStep === 1 && "システムにログインしてください"}
            {currentStep === 2 && "メニューをアップロードしてください"}
            {currentStep === 3 && "詳細設定を行ってください"}
            {currentStep === 4 && "お店の想いを教えてください"}
            {currentStep === 5 && "イチオシメニューを設定してください"}
            {currentStep === 6 && "おめでとうございます！"}
          </p>
        </div>
      </div>
    </div>
  );

  // Step 0: Plan Selection
  const PlanSelectionStep = () => {
    return (
      <div className="w-full max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-6">
            <Crown className="w-16 h-16 text-yellow-400 mr-4" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-yellow-400 bg-clip-text text-transparent">
              プラン選択
            </h1>
          </div>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            お店に最適なプランを選択して、世界中のお客様に素晴らしい体験を提供しましょう
          </p>
        </div>

        <div className="grid grid-cols-3 gap-8">
          {CONFIG.plans.map((plan) => (
            <div
              key={plan.id}
              className={`ps3-card p-8 cursor-pointer transition-all duration-300 relative ${
                selectedPlan === plan.id ? 'ps3-glow scale-105' : 'hover:scale-102'
              } ${plan.recommended ? 'border-2 border-yellow-400/50' : ''}`}
              onClick={() => setSelectedPlan(plan.id)}
            >
              {plan.recommended && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <div className="bg-gradient-to-r from-yellow-400 to-yellow-600 text-black px-4 py-1 rounded-full text-sm font-bold flex items-center">
                    <Star className="w-4 h-4 mr-1" />
                    おすすめ
                  </div>
                </div>
              )}
              
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-gray-300">{plan.description}</p>
              </div>
              
              <div className="space-y-3 mb-8">
                {plan.features.map((feature, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0" />
                    <span className="text-gray-300">{feature}</span>
                  </div>
                ))}
              </div>
              
              <div className={`w-6 h-6 rounded-full border-2 mx-auto ${
                selectedPlan === plan.id
                  ? 'bg-blue-500 border-blue-500'
                  : 'border-gray-400'
              }`}>
                {selectedPlan === plan.id && (
                  <CheckCircle className="w-6 h-6 text-white -mt-0.5 -ml-0.5" />
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="flex justify-center mt-12">
          <button
            onClick={() => setCurrentStep(1)}
            disabled={!selectedPlan}
            className={`ps3-button px-12 py-4 text-xl font-bold flex items-center space-x-3 ${
              !selectedPlan 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:scale-105'
            }`}
          >
            <Sparkles className="w-6 h-6" />
            <span>選択したプランで開始</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </div>
    );
  };

  // Step 1: Login
  const LoginStep = () => {
    const handleLogin = async () => {
      setIsLoading(true);
      setError("");
      
      try {
        const isValid = await authenticateCredentials(storeId, memberNumber);
        if (isValid) {
          setLoggedIn(true);
          setCurrentStep(2);
        } else {
          setError("ログイン情報が正しくありません");
        }
      } catch (err) {
        setError("ログインに失敗しました");
      } finally {
        setIsLoading(false);
      }
    };

    return (
      <div className="w-full max-w-md mx-auto">
        <div className="ps3-card p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-4">
              <Cpu className="w-12 h-12 text-blue-400 mr-3" />
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-blue-600 bg-clip-text text-transparent">
                TONOSAMA
              </h1>
            </div>
            <p className="text-gray-300 text-lg">東大レベル翻訳システム</p>
            <div className="w-16 h-0.5 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mt-4"></div>
          </div>
          
          <div className="space-y-6">
            <div className="space-y-2">
              <Label className="text-blue-300 flex items-center space-x-2">
                <Shield className="w-4 h-4" />
                <span>ストアID</span>
              </Label>
              <Input
                placeholder="例: TONOSAMA001"
                value={storeId}
                onChange={(e) => setStoreId(e.target.value)}
                className="ps3-input"
              />
            </div>
            
            <div className="space-y-2">
              <Label className="text-blue-300 flex items-center space-x-2">
                <Shield className="w-4 h-4" />
                <span>責任者ナンバー</span>
              </Label>
              <Input
                type="password"
                placeholder="例: 99999"
                value={memberNumber}
                onChange={(e) => setMemberNumber(e.target.value)}
                className="ps3-input"
              />
            </div>
            
            {error && (
              <div className="flex items-center space-x-2 ps3-error">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}
            
            <button
              onClick={handleLogin}
              disabled={isLoading || !storeId || !memberNumber}
              className={`ps3-button w-full py-4 text-lg font-semibold transition-all duration-300 ${
                isLoading || !storeId || !memberNumber 
                  ? 'opacity-50 cursor-not-allowed' 
                  : 'hover:scale-105'
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="ps3-loading"></div>
                  <span>認証中...</span>
                </div>
              ) : (
                <div className="flex items-center justify-center space-x-2">
                  <Zap className="w-5 h-5" />
                  <span>システムログイン</span>
                </div>
              )}
            </button>
            
            <div className="text-center text-sm text-blue-300 glass-effect p-4 rounded-lg">
              <Shield className="w-5 h-5 mx-auto mb-2" />
              あなたの情報は暗号化されて安全に保護されます
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Step 2: Menu Upload
  const MenuUploadStep = () => {
    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;
      
      setUploadedFile(file);
      setIsLoading(true);
      
      try {
        const extractedMenus = await performOCR(file);
        setMenus(extractedMenus);
      } catch (err) {
        setError("メニュー読み取りに失敗しました");
      } finally {
        setIsLoading(false);
      }
    };

    const updateMenu = (id: number, field: keyof MenuData, value: any) => {
      setMenus(prev => prev.map(menu => 
        menu.id === id ? { ...menu, [field]: value } : menu
      ));
    };

    const addNewMenu = () => {
      const newMenu: MenuData = {
        id: Date.now(),
        name: `新しいメニュー ${menus.length + 1}`,
        price: "0円",
        category: CONFIG.menuCategories[0],
        order: menus.length,
        allergens: [],
        multilingualDescriptions: { "日本語": "" },
        isFeatured: false,
        shouldIntroduce: true
      };
      setMenus(prev => [...prev, newMenu]);
    };

    const deleteMenu = (id: number) => {
      setMenus(prev => prev.filter(menu => menu.id !== id));
    };

    return (
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div className="ps3-card p-8">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-4">
              <Upload className="w-8 h-8 text-blue-400" />
              <h2 className="text-3xl font-bold">メニューアップロード</h2>
            </div>
            <p className="text-gray-300 text-lg">
              お店のメニュー表（画像またはPDF）をアップロードしてください
            </p>
          </div>
          
          <div className="space-y-6">
            <div className="border-2 border-dashed border-blue-400/30 rounded-xl p-12 text-center glass-effect hover:border-blue-400/50 transition-all duration-300">
              <Upload className="mx-auto mb-6 text-blue-400" size={64} />
              <Label htmlFor="menu-upload" className="cursor-pointer">
                <Input
                  id="menu-upload"
                  type="file"
                  accept="image/*,.pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                />
                <div className="ps3-button inline-flex items-center space-x-2 px-8 py-4 text-lg">
                  <Upload className="w-5 h-5" />
                  <span>ファイルを選択</span>
                </div>
              </Label>
              <p className="mt-4 text-gray-400">PNG, JPG, PDF (最大10MB)</p>
            </div>
            
            {uploadedFile && (
              <div className="text-center">
                <div className="ps3-success flex items-center justify-center space-x-2 text-lg">
                  <CheckCircle size={20} />
                  <span>ファイル: {uploadedFile.name}</span>
                </div>
              </div>
            )}
            
            {isLoading && (
              <div className="text-center">
                <div className="flex items-center justify-center space-x-3 text-blue-400 text-lg">
                  <div className="ps3-loading"></div>
                  <span>AI解析中...</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {menus.length > 0 && (
          <div className="ps3-card p-8">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-2xl font-bold">メニュー情報の編集</h3>
              <button onClick={addNewMenu} className="ps3-button px-6 py-3">
                ➕ 新規メニューを追加
              </button>
            </div>
            
            <div className="space-y-6">
              {menus.map((menu, index) => (
                <div key={menu.id} className="ps3-card p-6 hover:ps3-glow transition-all duration-300">
                  <div className="flex justify-between items-center mb-6">
                    <h4 className="text-xl font-semibold text-blue-300">
                      メニュー {index + 1}: {menu.name}
                    </h4>
                    <button
                      onClick={() => deleteMenu(menu.id)}
                      className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                    >
                      🗑️ 削除
                    </button>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-6">
                      <div>
                        <Label className="text-gray-300 mb-2 block">メニュー名</Label>
                        <Input
                          value={menu.name}
                          onChange={(e) => updateMenu(menu.id, 'name', e.target.value)}
                          className="ps3-input"
                        />
                      </div>
                      <div>
                        <Label className="text-gray-300 mb-2 block">価格</Label>
                        <Input
                          value={menu.price}
                          onChange={(e) => updateMenu(menu.id, 'price', e.target.value)}
                          className="ps3-input"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <Label className="text-gray-300 mb-2 block">カテゴリー</Label>
                      <Select
                        value={menu.category}
                        onValueChange={(value) => updateMenu(menu.id, 'category', value)}
                      >
                        <SelectTrigger className="ps3-input">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent className="glass-effect">
                          {CONFIG.menuCategories.map(cat => (
                            <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <div>
                      <Label className="text-gray-300 mb-3 block">アレルギー情報</Label>
                      <div className="grid grid-cols-4 gap-3">
                        {CONFIG.commonAllergens.map(allergen => (
                          <div key={allergen} className="flex items-center space-x-2">
                            <Checkbox
                              checked={menu.allergens.includes(allergen)}
                              onCheckedChange={(checked) => {
                                const newAllergens = checked
                                  ? [...menu.allergens, allergen]
                                  : menu.allergens.filter(a => a !== allergen);
                                updateMenu(menu.id, 'allergens', newAllergens);
                              }}
                              className="border-blue-400"
                            />
                            <Label className="text-sm text-gray-300">{allergen}</Label>
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3">
                      <Checkbox
                        checked={menu.shouldIntroduce}
                        onCheckedChange={(checked) => updateMenu(menu.id, 'shouldIntroduce', checked)}
                        className="border-blue-400"
                      />
                      <Label className="text-gray-300">このメニューを掲載する</Label>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-between">
          <button
            onClick={() => setCurrentStep(1)}
            className="ps3-button px-6 py-3 bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <ArrowLeft size={16} />
            <span>戻る</span>
          </button>
          <button
            onClick={() => setCurrentStep(3)}
            disabled={menus.filter(m => m.shouldIntroduce).length === 0}
            className={`ps3-button px-6 py-3 flex items-center space-x-2 ${
              menus.filter(m => m.shouldIntroduce).length === 0 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:scale-105'
            }`}
          >
            <span>次へ進む</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  };

  // Step 3: Detail Settings
  const DetailSettingsStep = () => {
    return (
      <div className="w-full max-w-4xl mx-auto">
        <div className="ps3-card p-8">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-4">
              <Shield className="w-8 h-8 text-blue-400" />
              <h2 className="text-3xl font-bold">詳細設定</h2>
            </div>
            <p className="text-gray-300 text-lg">
              アレルギー情報に関する表示ポリシーを総合的に設定してください
            </p>
          </div>
          
          <div className="space-y-8">
            <div className="space-y-6">
              <Label className="text-blue-300 text-xl">アレルギー情報表示ポリシー</Label>
              <div className="space-y-4">
                {[
                  { 
                    value: "display", 
                    label: "全メニューにアレルギー情報を表示する",
                    description: "各メニューにアレルギー成分を詳細に表示します"
                  },
                  { 
                    value: "hide", 
                    label: "アレルギー情報は表示しない",
                    description: "メニュー表にはアレルギー情報を含めません"
                  },
                  { 
                    value: "disclaimer_only", 
                    label: "店内の注意書きのみとする",
                    description: "個別表示はせず、総合的な注意事項のみ記載します"
                  }
                ].map(option => (
                  <div key={option.value} className="glass-effect p-6 rounded-lg hover:bg-white/10 transition-all cursor-pointer">
                    <div className="flex items-start space-x-4">
                      <input
                        type="radio"
                        id={option.value}
                        name="allergy-policy"
                        value={option.value}
                        checked={allergyPolicy === option.value}
                        onChange={(e) => setAllergyPolicy(e.target.value as any)}
                        className="w-5 h-5 mt-1 text-blue-400 border-gray-300 focus:ring-blue-500"
                      />
                      <div className="flex-1">
                        <Label htmlFor={option.value} className="text-white text-lg font-medium cursor-pointer">
                          {option.label}
                        </Label>
                        <p className="text-gray-400 mt-1">{option.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {allergyPolicy === "disclaimer_only" && (
              <div className="space-y-4">
                <Label className="text-blue-300 text-lg">店内でのアレルギー対応について</Label>
                <Textarea
                  value={allergyDisclaimer}
                  onChange={(e) => setAllergyDisclaimer(e.target.value)}
                  placeholder="例: アレルギーをお持ちのお客様は、ご来店時にスタッフまでお申し出ください。可能な限り対応させていただきます。"
                  rows={4}
                  className="ps3-input resize-none"
                />
                <p className="text-sm text-gray-400 flex items-center space-x-2">
                  <Mic className="w-4 h-4" />
                  <span>ご自身のスマホの音声ボタンからも入力可能です</span>
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={() => setCurrentStep(2)}
            className="ps3-button px-6 py-3 bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <ArrowLeft size={16} />
            <span>戻る</span>
          </button>
          <button
            onClick={() => setCurrentStep(4)}
            className="ps3-button px-6 py-3 flex items-center space-x-2 hover:scale-105"
          >
            <span>次へ進む</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  };

  // Step 4: Owner Thoughts
  const OwnerThoughtsStep = () => {
    const questionSections = [
      {
        title: "🏪 お店の基本情報",
        questions: [
          {
            key: "restaurant_name",
            label: "お店の名前を教えてください",
            placeholder: "例: 和食処 さくら",
            type: "input"
          },
          {
            key: "years_in_business",
            label: "お店を開いてから何年になりますか?",
            placeholder: "例: 10年になります",
            type: "input"
          },
          {
            key: "location_features",
            label: "お店の場所・立地の特徴を教えてください",
            placeholder: "例: 駅から徒歩3分、商店街の中にあります",
            type: "textarea"
          }
        ]
      },
      {
        title: "💭 お店の想い・こだわり",
        questions: [
          {
            key: "concept",
            label: "お店のコンセプトや想いを教えてください",
            placeholder: "例: 家庭的な温かい雰囲気で、心のこもった料理を提供したい",
            type: "textarea"
          },
          {
            key: "ingredient_commitment",
            label: "特にこだわっている食材や調理法はありますか?",
            placeholder: "例: 地元の野菜を使用し、手作りにこだわっています",
            type: "textarea"
          },
          {
            key: "service_approach",
            label: "お客様に対してどのようなサービスを心がけていますか?",
            placeholder: "例: 一人一人のお客様との会話を大切にしています",
            type: "textarea"
          }
        ]
      },
      {
        title: "🍽️ 料理・メニューについて",
        questions: [
          {
            key: "signature_dish",
            label: "お店の看板メニューとその特徴を教えてください",
            placeholder: "例: 手作りハンバーグは祖母から受け継いだレシピです",
            type: "textarea"
          },
          {
            key: "seasonal_menus",
            label: "季節ごとのメニューやイベントはありますか?",
            placeholder: "例: 春は山菜料理、夏は冷やし中華に力を入れています",
            type: "textarea"
          },
          {
            key: "menu_development",
            label: "新しいメニューを考える時に大切にしていることは?",
            placeholder: "例: お客様の声を聞いて、健康的で美味しい料理を考えています",
            type: "textarea"
          }
        ]
      },
      {
        title: "🌏 国際的なお客様について",
        questions: [
          {
            key: "international_experience",
            label: "海外のお客様にどのような体験をしてほしいですか?",
            placeholder: "例: 日本の家庭料理の温かさを感じてほしいです",
            type: "textarea"
          },
          {
            key: "cultural_sharing",
            label: "お店の文化や料理の背景で伝えたいことはありますか?",
            placeholder: "例: 手作りの大切さと、食材への感謝の気持ちを伝えたいです",
            type: "textarea"
          },
          {
            key: "international_message",
            label: "海外からのお客様へのメッセージをお聞かせください",
            placeholder: "例: 日本の味を楽しんでいただき、素敵な思い出を作ってください",
            type: "textarea"
          }
        ]
      },
      {
        title: "🚀 今後の展望",
        questions: [
          {
            key: "future_goals",
            label: "今後のお店の目標や夢を教えてください",
            placeholder: "例: 地域の人々と海外の方々の交流の場になりたいです",
            type: "textarea"
          },
          {
            key: "multilingual_expectations",
            label: "多言語メニューでどのような効果を期待されますか?",
            placeholder: "例: 言葉の壁を越えて、より多くの方に料理を楽しんでもらいたいです",
            type: "textarea"
          },
          {
            key: "customer_message",
            label: "最後に、お客様への一言メッセージをお願いします",
            placeholder: "例: 心を込めて作った料理で、皆様に笑顔をお届けします",
            type: "textarea"
          }
        ]
      }
    ];

    const canProceed = questionSections.every(section =>
      section.questions.every(q => ownerAnswers[q.key as keyof OwnerAnswers]?.trim())
    );

    const filledCount = questionSections.reduce((total, section) =>
      total + section.questions.filter(q => ownerAnswers[q.key as keyof OwnerAnswers]?.trim()).length, 0
    );

    return (
      <div className="w-full max-w-5xl mx-auto">
        <div className="ps3-card p-8">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-4">
              <Star className="w-8 h-8 text-blue-400" />
              <h2 className="text-3xl font-bold">15問の質問にお答えいただき、お店の想いを世界に伝えましょう!</h2>
            </div>
            <p className="text-xl text-blue-300 font-medium mb-4">
              **質問に答えて、お店の想いを教えてください**
            </p>
            <div className="glass-effect p-4 rounded-lg">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">回答進捗</span>
                <span className="text-blue-300 font-bold">{filledCount}/15 完了</span>
              </div>
              <div className="ps3-progress h-2 mt-2">
                <div 
                  className="ps3-progress-bar h-full transition-all duration-500"
                  style={{ width: `${(filledCount / 15) * 100}%` }}
                />
              </div>
            </div>
            <p className="text-sm text-gray-400 mt-4 flex items-center space-x-2">
              <Mic className="w-4 h-4" />
              <span>ご自身のスマホの音声ボタンからも入力可能です</span>
            </p>
          </div>
          
          <div className="space-y-12">
            {questionSections.map((section, sectionIndex) => (
              <div key={sectionIndex} className="space-y-6">
                <h3 className="text-2xl font-bold text-yellow-400 mb-6">{section.title}</h3>
                
                <div className="space-y-8">
                  {section.questions.map((question) => (
                    <div key={question.key} className="space-y-3">
                      <Label className="text-blue-300 text-lg font-medium">
                        {question.label}
                      </Label>
                      <div className="space-y-2">
                        <p className="text-sm text-gray-400">
                          <strong>回答例:</strong> {question.placeholder}
                        </p>
                        {question.type === "input" ? (
                          <Input
                            value={ownerAnswers[question.key as keyof OwnerAnswers] || ""}
                            onChange={(e) => updateAnswer(question.key as keyof OwnerAnswers, e.target.value)}
                            placeholder={question.placeholder}
                            className="ps3-input text-lg"
                          />
                        ) : (
                          <Textarea
                            value={ownerAnswers[question.key as keyof OwnerAnswers] || ""}
                            onChange={(e) => updateAnswer(question.key as keyof OwnerAnswers, e.target.value)}
                            placeholder={question.placeholder}
                            rows={4}
                            className="ps3-input resize-none text-lg"
                          />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-between mt-8">
          <button
            onClick={() => setCurrentStep(3)}
            className="ps3-button px-6 py-3 bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <ArrowLeft size={16} />
            <span>戻る</span>
          </button>
          <button
            onClick={() => setCurrentStep(5)}
            disabled={!canProceed}
            className={`ps3-button px-6 py-3 flex items-center space-x-2 ${
              !canProceed 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:scale-105'
            }`}
          >
            <span>次へ進む</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  };

  // Step 5: Featured Menus
  const FeaturedMenusStep = () => {
    const updateFeaturedMenu = (id: number, field: keyof MenuData, value: any) => {
      setFeaturedMenus(prev => prev.map(menu => 
        menu.id === id ? { ...menu, [field]: value } : menu
      ));
      setMenus(prev => prev.map(menu => 
        menu.id === id ? { ...menu, [field]: value } : menu
      ));
    };

    const handleFeaturedSelection = (menuId: number, checked: boolean) => {
      const menu = menus.find(m => m.id === menuId);
      if (!menu) return;

      if (checked) {
        setFeaturedMenus(prev => [...prev, { ...menu, isFeatured: true }]);
      } else {
        setFeaturedMenus(prev => prev.filter(m => m.id !== menuId));
      }
      
      setMenus(prev => prev.map(m => 
        m.id === menuId ? { ...m, isFeatured: checked } : m
      ));
    };

    return (
      <div className="w-full max-w-6xl mx-auto space-y-8">
        <div className="ps3-card p-8">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-4">
              <Star className="w-8 h-8 text-yellow-400" />
              <h2 className="text-3xl font-bold">イチオシメニュー設定</h2>
            </div>
            <p className="text-gray-300 text-lg">
              お店のイチオシメニューを選択し、詳細情報を設定してください
            </p>
          </div>
          
          <div className="space-y-6">
            <Label className="text-blue-300 text-lg">イチオシメニューを選択してください</Label>
            <div className="grid grid-cols-2 gap-4">
              {menus.filter(m => m.shouldIntroduce).map(menu => (
                <div key={menu.id} className="glass-effect p-4 rounded-lg hover:bg-white/10 transition-all">
                  <div className="flex items-center space-x-3">
                    <Checkbox
                      checked={featuredMenus.some(fm => fm.id === menu.id)}
                      onCheckedChange={(checked) => handleFeaturedSelection(menu.id, !!checked)}
                      className="border-blue-400"
                    />
                    <div>
                      <p className="font-medium text-white">{menu.name}</p>
                      <p className="text-sm text-gray-400">{menu.price}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {featuredMenus.length > 0 && (
          <div className="ps3-card p-8">
            <h3 className="text-2xl font-bold mb-8 text-yellow-400">イチオシメニュー詳細設定</h3>
            
            <div className="space-y-8">
              {featuredMenus.map(menu => (
                <div key={menu.id} className="ps3-card p-6 border-2 border-yellow-400/30 bg-gradient-to-r from-yellow-400/10 to-yellow-600/10">
                  <div className="flex items-center space-x-3 mb-6">
                    <Star className="text-yellow-400" size={24} />
                    <h4 className="text-xl font-bold text-yellow-300">{menu.name}</h4>
                  </div>
                  
                  <div className="space-y-6">
                    <div>
                      <Label className="text-gray-300 mb-2 block">イチオシメニュー用画像URL</Label>
                      <Input
                        value={menu.imageUrl || ""}
                        onChange={(e) => updateFeaturedMenu(menu.id, 'imageUrl', e.target.value)}
                        placeholder="https://example.com/menu_image.jpg"
                        className="ps3-input"
                      />
                    </div>
                    
                    <div>
                      <Label className="text-gray-300 mb-2 block">日本語説明文</Label>
                      <Textarea
                        value={menu.multilingualDescriptions["日本語"] || ""}
                        onChange={(e) => {
                          const newDescriptions = { 
                            ...menu.multilingualDescriptions, 
                            "日本語": e.target.value 
                          };
                          updateFeaturedMenu(menu.id, 'multilingualDescriptions', newDescriptions);
                        }}
                        placeholder={`${menu.name}の魅力的な説明をどうぞ`}
                        rows={4}
                        className="ps3-input resize-none"
                      />
                      <p className="text-sm text-gray-400 mt-2 flex items-center space-x-2">
                        <Mic className="w-4 h-4" />
                        <span>ご自身のスマホの音声ボタンからも入力可能です</span>
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-between">
          <button
            onClick={() => setCurrentStep(4)}
            className="ps3-button px-6 py-3 bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <ArrowLeft size={16} />
            <span>戻る</span>
          </button>
          <button
            onClick={() => setCurrentStep(6)}
            className="ps3-button px-6 py-3 flex items-center space-x-2 hover:scale-105"
          >
            <span>次へ進む</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>
    );
  };

  // Step 6: Completion
  const CompletionStep = () => {
    const handleCompletion = async () => {
      setIsLoading(true);
      try {
        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        setIsCompleted(true);
      } catch (err) {
        setError("完成処理に失敗しました");
      } finally {
        setIsLoading(false);
      }
    };

    if (isCompleted) {
      return (
        <div className="w-full max-w-4xl mx-auto space-y-8">
          <div className="ps3-card p-8 text-center">
            <div className="mb-8">
              <div className="flex items-center justify-center mb-6">
                <Gift className="w-20 h-20 text-green-400 mr-4" />
                <div>
                  <h1 className="text-6xl font-bold bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                    完成！
                  </h1>
                  <p className="text-2xl text-green-300">
                    🎉 おめでとうございます！🎉
                  </p>
                </div>
              </div>
              <p className="text-xl text-gray-300 mb-8">
                多言語メニューの準備が完了しました！<br/>
                世界中のお客様に素晴らしい体験をお届けください！
              </p>
            </div>

            <div className="space-y-6">
              <div className="glass-effect p-6 rounded-lg">
                <h3 className="text-2xl font-bold text-blue-300 mb-4">完了内容</h3>
                <div className="grid grid-cols-2 gap-6 text-left">
                  <div>
                    <p><span className="text-blue-300">プラン:</span> {CONFIG.plans.find(p => p.id === selectedPlan)?.name}</p>
                    <p><span className="text-blue-300">店名:</span> {ownerAnswers.restaurant_name}</p>
                    <p><span className="text-blue-300">メニュー数:</span> {menus.filter(m => m.shouldIntroduce).length}品</p>
                  </div>
                  <div>
                    <p><span className="text-blue-300">イチオシ:</span> {featuredMenus.length}品</p>
                    <p><span className="text-blue-300">想いの回答:</span> 15/15 完了</p>
                    <p><span className="text-blue-300">アレルギー設定:</span> 完了</p>
                  </div>
                </div>
              </div>

              <div className="text-2xl text-green-300 font-bold">
                システム処理が完了しました！
              </div>
              
              <p className="text-lg text-gray-300">
                多言語対応メニューの作成が正常に完了いたしました。<br/>
                素晴らしいお店作りを心より応援しております！
              </p>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="w-full max-w-4xl mx-auto space-y-8">
        <div className="ps3-card p-8">
          <div className="text-center mb-8">
            <div className="flex items-center justify-center mb-6">
              <Gift className="w-16 h-16 text-green-400 mr-4" />
              <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
                完成！
              </h1>
            </div>
            <p className="text-xl text-gray-300">
              いよいよ最終ステップです！
            </p>
          </div>
          
          <div className="space-y-8">
            <div>
              <h3 className="text-xl font-semibold mb-6 text-blue-300">入力内容サマリー</h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="glass-effect p-6 rounded-lg">
                  <h4 className="font-semibold text-blue-300 mb-4">店舗情報</h4>
                  <div className="space-y-2 text-gray-300">
                    <p><span className="text-blue-300">プラン:</span> {CONFIG.plans.find(p => p.id === selectedPlan)?.name}</p>
                    <p><span className="text-blue-300">店舗ID:</span> {storeId}</p>
                    <p><span className="text-blue-300">店名:</span> {ownerAnswers.restaurant_name}</p>
                    <p><span className="text-blue-300">メニュー数:</span> {menus.filter(m => m.shouldIntroduce).length}品</p>
                    <p><span className="text-blue-300">イチオシ:</span> {featuredMenus.length}品</p>
                  </div>
                </div>
                
                <div className="glass-effect p-6 rounded-lg">
                  <h4 className="font-semibold text-blue-300 mb-4">設定情報</h4>
                  <div className="space-y-2 text-gray-300">
                    <p><span className="text-blue-300">アレルギー表示:</span> {
                      allergyPolicy === "display" ? "表示する" :
                      allergyPolicy === "hide" ? "表示しない" : "注意書きのみ"
                    }</p>
                    <p><span className="text-blue-300">想いの回答:</span> 15/15 完了</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="w-full h-px bg-gradient-to-r from-transparent via-blue-400 to-transparent"></div>

            <div className="text-center space-y-6">
              <button
                onClick={handleCompletion}
                disabled={isLoading}
                className={`ps3-button px-16 py-6 text-2xl font-bold ${
                  isLoading 
                    ? 'opacity-50 cursor-not-allowed' 
                    : 'hover:scale-105'
                }`}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center space-x-3">
                    <div className="ps3-loading"></div>
                    <span>処理中...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center space-x-3">
                    <Sparkles className="w-8 h-8" />
                    <span>完成！</span>
                  </div>
                )}
              </button>
              
              <p className="text-gray-400">
                ボタンを押すと多言語メニューの作成が完了します
              </p>
            </div>
          </div>
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setCurrentStep(5)}
            className="ps3-button px-6 py-3 bg-gray-600 hover:bg-gray-700 flex items-center space-x-2"
          >
            <ArrowLeft size={16} />
            <span>戻る</span>
          </button>
          <div></div>
        </div>
      </div>
    );
  };

  // Main render
  return (
    <div className="min-h-screen p-6 relative overflow-hidden">
      {/* Background effects */}
      <div className="fixed inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-black -z-10"></div>
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(74,144,226,0.1),transparent_70%)] -z-10"></div>
      
      <Navigation />
      
      <div className="flex justify-center relative z-10">
        {currentStep === 0 && <PlanSelectionStep />}
        {currentStep === 1 && !loggedIn && <LoginStep />}
        {currentStep === 2 && loggedIn && <MenuUploadStep />}
        {currentStep === 3 && <DetailSettingsStep />}
        {currentStep === 4 && <OwnerThoughtsStep />}
        {currentStep === 5 && <FeaturedMenusStep />}
        {currentStep === 6 && <CompletionStep />}
      </div>
    </div>
  );
}
