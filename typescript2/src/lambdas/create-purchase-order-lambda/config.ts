import { z } from "zod";

const environmentSchema = z.enum(["development", "production"]);

const environmentConfigSchema = z.object({
  environment: environmentSchema,
  s3Options: z.object({
    region: z.string(),
  }),
});

export type EnvironmentConfig = z.infer<typeof environmentConfigSchema>;

export const getConfig = (): EnvironmentConfig => {
  const environment = environmentSchema.parse(process.env.ENVIRONMENT);

  return environmentConfigSchema.parse({
    environment,
    ...(environment === "production" || environment === "development"
      ? {
        s3Options: {
            region: "sa-east-1",
          },
        }
      : {
        s3Options: {
            region: "sa-east-1",
          },
        }),
  });
};

export const config = getConfig();
