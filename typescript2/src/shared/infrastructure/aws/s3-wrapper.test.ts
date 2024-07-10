// https://stackoverflow.com/questions/63587868/how-can-i-mock-a-private-property-in-a-class-im-trying-to-test-in-jest

// // const mockGetIdToken = jest.fn(() => 'abc123');

// import { S3Client } from "@aws-sdk/client-s3";
import { PutObjectCommandInput, S3Client } from "@aws-sdk/client-s3";
import { S3Wrapper } from "./s3-wrapper";

// jest.mock("./s3-wrapper", () => {
//   return jest.fn().mockImplementation(() => ({
//     s3Client: "a",
//   }));
// });

// const mTableName = {
// 	send: jest.fn().mockReturnThis()
// };

// jest.mock("@aws-sdk/client-s3", () => {
//   return {
//     S3Client: jest.fn(() => mTableName),
//     PutObjectCommand: jest.fn(() => {}),
//   };
// });

// jest.mock("./s3-wrapper");

// const mTableName = {
// 	send: jest.fn().mockReturnThis()
// };

// jest.mock("./s3-wrapper", () => ({
// 	s3Client: mTableName
// }))

describe("A", () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  describe("", () => {
    it("", async () => {
      const config = {
        s3Options: {
          region: "sa-east-1",
        },
      };

      const params: PutObjectCommandInput = {
        Bucket: undefined,
        Body: undefined,
        Key: "",
      };

      // const mockLogger = new S3Client(config);
      // const sendMock = jest
      // .spyOn(mockLogger, 'send')
      // .mockImplementation((params) => {});

      // mTableName.send.mockResolvedValueOnce('fake response');

      const s3Wrapper = new S3Wrapper(config);

			// s3Wrapper["s3Client"] = {
			// 		config: jest.mock(),
			// 	  send: jest.fn().mockResolvedValue("fake response"),
			// 	};

			Reflect.set(s3Wrapper, 's3Client',  {
				  send: jest.fn().mockResolvedValue("fake response"),
				});

      // (s3Wrapper as any).s3Client = {
      //   send: jest.fn().mockResolvedValue("fake response"),
      // };

      // jest.mocked(s3Wrapper["s3Client"]).send.mockResolvedValue('fake response');

      const result = await s3Wrapper.putObject(params);

      expect(result).toEqual("fake response");
      // expect(s3ClientInstance.send).toHaveBeenCalledTimes(1);
      // expect(putObjectCommandInstance).toHaveBeenCalledWith<
      //   Parameters<typeof putObject>
      // >(params);
    });
  });
});
