import { makeApi, Zodios, type ZodiosOptions } from "@zodios/core";
import { z } from "zod";

const Input = z
  .object({
    words: z.array(z.array(z.string())),
    rank_n: z.number().int().optional().default(1),
  })
  .passthrough();
const Abbrs = z.object({ abbrs: z.array(z.array(z.string())) }).passthrough();
const ValidationError = z
  .object({
    loc: z.array(z.union([z.string(), z.number()])),
    msg: z.string(),
    type: z.string(),
  })
  .passthrough();
const HTTPValidationError = z
  .object({ detail: z.array(ValidationError) })
  .partial()
  .passthrough();

export const schemas = {
  Input,
  Abbrs,
  ValidationError,
  HTTPValidationError,
};

const endpoints = makeApi([
  {
    method: "get",
    path: "/",
    alias: "index__get",
    requestFormat: "json",
    response: z.unknown(),
  },
  {
    method: "get",
    path: "/:path",
    alias: "web_path__path__get",
    requestFormat: "json",
    parameters: [
      {
        name: "path",
        type: "Path",
        schema: z.string(),
      },
    ],
    response: z.unknown(),
    errors: [
      {
        status: 422,
        description: `Validation Error`,
        schema: HTTPValidationError,
      },
    ],
  },
  {
    method: "post",
    path: "/api",
    alias: "api_api_post",
    requestFormat: "json",
    parameters: [
      {
        name: "body",
        type: "Body",
        schema: Input,
      },
    ],
    response: Abbrs,
    errors: [
      {
        status: 422,
        description: `Validation Error`,
        schema: HTTPValidationError,
      },
    ],
  },
]);

export const api = new Zodios(endpoints);

export function createApiClient(baseUrl: string, options?: ZodiosOptions) {
  return new Zodios(baseUrl, endpoints, options);
}
