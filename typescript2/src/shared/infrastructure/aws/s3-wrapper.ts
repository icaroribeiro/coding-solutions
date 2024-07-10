import {
  S3Client,
  PutObjectCommandInput,
  PutObjectCommandOutput,
  PutObjectCommand,
  ListObjectsCommand,
  ListObjectsCommandInput,
  ListObjectsCommandOutput
} from '@aws-sdk/client-s3';



export class S3Wrapper {
  private s3Client: S3Client;


  constructor(config: any) {
    this.s3Client = new S3Client(config.s3Options)
  }

  public putObject = async (
    params: PutObjectCommandInput,
  ): Promise<PutObjectCommandOutput> => 
    await this.s3Client.send(new PutObjectCommand(params));


  // public listObject  = async (
  //   params: ListObjectsCommandInput,
  // ): Promise<ListObjectsCommandOutput> =>
  //   await this.s3Client.send(new ListObjectsCommand(params));
}
