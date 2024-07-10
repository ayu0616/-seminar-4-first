import { FormInput } from "@/components/FormInput/FormInput";
import { Button } from "@/components/ui/button";
import { Form } from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoaderIcon, PlusIcon, SendIcon, Trash2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

const schema = z.object({
    words: z
        .array(
            z
                .array(z.string().refine((val) => val.match(/^[ァ-ヴー]*$/u), { message: "全角カタカナで入力してください" }))
                .length(3)
                .transform((val) => {
                    const res = val.map((v) => v.trim()).filter((v) => v !== "");
                    for (let i = res.length; i < 3; i++) {
                        res.push("");
                    }
                    return res;
                })
        )
        .transform((val) => val.filter((v) => v.some((w) => w !== "")))
        .superRefine((val, ctx) => val.length > 0 || ctx.addIssue({ message: "最低1つ以上の単語を入力してください", path: [0, 0], code: "custom" })),
});
export type WordFormValues = z.infer<typeof schema>;

export interface WordFormProps {
    onSubmit: (data: WordFormValues) => void;
}

export const WordForm = ({ onSubmit }: WordFormProps) => {
    const form = useForm<WordFormValues>({
        resolver: zodResolver(schema),
        defaultValues: {
            words: [["", "", ""]],
        },
    });

    const disabled = form.formState.isSubmitting;

    return (
        <Form {...form}>
            <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
                {form.watch("words").map((elem, i) => (
                    <div className="flex w-full gap-1">
                        {elem.map((_word, j) => (
                            <div className="flex-1" key={j}>
                                <FormInput {...form.register(`words.${i}.${j}` as const)} disabled={disabled} />
                            </div>
                        ))}
                        <Button
                            type="button"
                            disabled={disabled}
                            variant="outline"
                            onClick={() => {
                                const newVal = form.getValues("words").filter((_, k) => k !== i);
                                if (newVal.length === 0) {
                                    form.setValue("words", [["", "", ""]]);
                                    return;
                                }
                                form.setValue("words", newVal);
                            }}
                            className="flex items-center gap-1 text-red-600 hover:text-red-700 hover:bg-red-50 hover:border-red-700"
                        >
                            <Trash2Icon size={16} />
                        </Button>
                    </div>
                ))}
                <div className="flex gap-2 w-full justify-end">
                    <Button
                        disabled={disabled}
                        type="button"
                        variant="outline"
                        onClick={() => form.setValue("words", [...form.getValues("words"), ["", "", ""]])}
                    >
                        <PlusIcon className="mr-1" size={16} />
                        <span>追加</span>
                    </Button>
                    <Button type="submit" disabled={disabled}>
                        {form.formState.isSubmitting ? (
                            <LoaderIcon className="animate-spin" size={16} />
                        ) : (
                            <>
                                <SendIcon className="mr-1" size={16} />
                                <span>送信</span>
                            </>
                        )}
                    </Button>
                </div>
            </form>
        </Form>
    );
};
