//
//  ServiceHelper.swift
//  Rojak
//
//  Created by Adi Nugroho on 10/27/16.
//  Copyright © 2016 Rojak Team. All rights reserved.
//

import Foundation
import Alamofire

class ServiceHelper {
    typealias onCompleteRequest = (DataResponse<Any>) -> Void
    
    static let baseUrl = "https://api.rojak.com/v1"
    
    class func request(_ endpoint: Endpoint, id: String?, isSentiment: Bool = false, completionHandler: @escaping onCompleteRequest ) {
        var url = "\(baseUrl)/" + "\(endpoint.rawValue)"
        
        if let id = id {
            url = "\(url)/" + "\(id)"
        }
        
        if isSentiment {
            url = "\(url)/media-sentiments"
        }
        
        Alamofire.request(url).responseJSON(completionHandler: completionHandler)
    }
}
