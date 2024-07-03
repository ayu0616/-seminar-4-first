import { useState } from "react";
import { WordForm, WordFormValues } from "./components/WordForm/WordForm";

function App() {
    const [words, setWords] = useState<string[]>([]);
    const [res, setRes] = useState<string[][]>([]);

    const handleSubmit = async (data: WordFormValues) => {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setWords(() => data.words.map((w) => w.join("")));
        setRes(() => {
            return data.words.map((w) => {
                const word = w.join("");
                return new Array(5).fill("").map(() =>
                    word
                        .split("")
                        .map((c) => (Math.random() < 0.5 ? c : ""))
                        .join("")
                );
            });
        });
    };

    return (
        <main className="bg-slate-50 min-h-dvh">
            <div className="max-w-2xl mx-auto px-4 py-8 space-y-6">
                <h1 className="font-bold text-xl">略語推定</h1>
                <div className="p-4 space-y-6 bg-white border rounded-md">
                    <ul className="list-disc list-inside">
                        <li>略語を入力してください</li>
                        <li>入力はカタカナのみ対応</li>
                        <li>
                            <div className="inline-flex items-center">
                                <span className="mr-2">要素ごとに入力してください：</span>
                                <span className="text-sm border p-0.5 rounded-sm mr-2">パーソナル</span>
                                <span className="text-sm border p-0.5 rounded-sm">コンピューター</span>
                            </div>
                        </li>
                    </ul>
                    <WordForm onSubmit={handleSubmit} />
                </div>
                {words.length > 0 && (
                    <div className="bg-white border rounded-md overflow-hidden">
                        <table className="w-full">
                            <thead className="border-b bg-slate-200 text-slate-700">
                                <tr>
                                    <th className="py-2 px-4">単語</th>
                                    <th className="py-2 px-4">結果</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {words.map((w, i) => (
                                    <tr key={i}>
                                        <td className="py-2 px-4">{w}</td>
                                        <td className="py-2 px-4">
                                            <ol className="list-decimal list-inside ml-6">
                                                {res[i].map((r, j) => (
                                                    <li key={j}>{r}</li>
                                                ))}
                                            </ol>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </main>
    );
}

export default App;
