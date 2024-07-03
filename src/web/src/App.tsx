import { useState } from "react";
import { WordForm, WordFormValues } from "./components/WordForm/WordForm";

function App() {
    const [res, setRes] = useState<string[]>([]);

    const handleSubmit = async (data: WordFormValues) => {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setRes(() => {
            return data.words.map((w) => {
                const word = w.join("");
                return word
                    .split("")
                    .map((c) => (Math.random() < 0.5 ? c : ""))
                    .join("");
            });
        });
    };

    return (
        <main className="bg-slate-50 min-h-dvh">
            <div className="p-4 max-w-2xl mx-auto">
                <WordForm onSubmit={handleSubmit} />
                {res.length > 0 && (
                    <div className="mt-4 p-4 bg-white rounded-md shadow">
                        <h2 className="text-lg font-bold">Results</h2>
                        <ul className="mt-2">
                            {res.map((r, i) => (
                                <li key={i}>{r}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </main>
    );
}

export default App;
