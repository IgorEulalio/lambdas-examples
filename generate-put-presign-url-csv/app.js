// Instancie o S3 client fora da funcao
// Boa pratica, para reuso do context 
// em funcoes paralelas
const AWS = require('aws-sdk')
// CREATE REGION ENVIRONMENT VARIABLE
// DEVE SER A MESMA EM QUE O SEU BUCKET ESTA CRIADO
// POR DEFAULT O CLIENT AWS PEGARA A REGION 
// DE EXECUCAO DA SUA LAMBDA
AWS.config.update({ region: process.env.REGION })

const s3 = new AWS.S3();

// CREATE S3_BUCKET_NAME ENVIRONMENT VARIABLE
const uploadBucket = process.env.S3_BUCKET_NAME

exports.handler = async (event) => {
  const result = await getUploadURL()
  return result
};

const getUploadURL = async function() {
  
  let actionId = Date.now()

  var s3Params = {
    Bucket: uploadBucket,
    Key:  `poc_${actionId}.csv`,
    ContentType: 'text/csv',
  };

  return new Promise((resolve, reject) => {
    let putPresignUrl = s3.getSignedUrl('putObject', s3Params)
    resolve({
      "statusCode": 200,
      "isBase64Encoded": false,
      "headers": {
        "Access-Control-Allow-Origin": "*"
      },
      "body": JSON.stringify({
          "uploadURL": putPresignUrl,
          "photoFilename": `poc_${actionId}.csv`
      })
    })
  })
}

